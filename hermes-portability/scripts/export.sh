#!/usr/bin/env bash
# Export a Hermes installation into a portable backup.
#
# Usage:
#   bash export.sh [--tier config|state|full] [--out DIR] [--with-plugins] [--no-mem0-service]
#
# Tiers (cumulative): config < state (default) < full
#   config  config, skills, hooks, cron, mem0 plugin, .env keys
#   state   config + memories/sessions/state.db/kanban.db/shared-state.db
#   full    state + hermes-agent source, installs, tools, skins
#
# mem0 is treated as first-class: the plugin code, its config entry, its env key,
# and the external mem0 Docker stack (compose + .env keys + pg_dump) are all captured.
#
# Env:
#   HERMES_HOME   default: $HOME/.hermes
#
# Never copies secrets: .env becomes .env.example (keys only), auth.json is skipped.
set -euo pipefail

TIER="state"
OUT=""
WITH_PLUGINS=0
WITH_MEM0_SERVICE=1
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
MEM0_SERVICE_DIR="${MEM0_SERVICE_DIR:-$HOME/mem0/server}"

usage() {
  sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

while [ $# -gt 0 ]; do
  case "$1" in
    --tier) TIER="${2:-}"; shift 2 ;;
    --out)  OUT="${2:-}";  shift 2 ;;
    --with-plugins) WITH_PLUGINS=1; shift ;;
    --no-mem0-service) WITH_MEM0_SERVICE=0; shift ;;
    -h|--help) usage ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

case "$TIER" in
  config|state|full) ;;
  *) echo "--tier must be one of: config, state, full" >&2; exit 2 ;;
esac

PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then echo "python3 not found (needed for SQLite backup + manifest)" >&2; exit 1; fi
if [ ! -d "$HERMES_HOME" ]; then echo "HERMES_HOME not found: $HERMES_HOME" >&2; exit 1; fi

[ -n "$OUT" ] || OUT="$HOME/hermes-backup"
STAMP="$(date +%Y%m%d-%H%M)"
DEST="$OUT/hermes-$STAMP"
ROOT="$DEST/files/hermes"
mkdir -p "$ROOT"

CONFIG_ITEMS=(config.yaml SOUL.md channel_directory.json desktop-plugins hooks skills cron)
STATE_ITEMS=(memories sessions)
DB_ITEMS=(state.db kanban.db shared-state.db)
FULL_ITEMS=(hermes-agent installs tools skins)

copy_path() {
  local rel="$1"
  [ -e "$HERMES_HOME/$rel" ] || return 0
  mkdir -p "$ROOT/$(dirname "$rel")"
  cp -a "$HERMES_HOME/$rel" "$ROOT/$rel"
  echo "  + $rel"
}

copy_tree_filtered() {
  local rel="$1"
  [ -d "$HERMES_HOME/$rel" ] || return 0
  mkdir -p "$ROOT"
  # cd into the directories instead of tar -C: Windows paths passed via -C
  # are mangled by GNU tar's backslash escaping.
  (
    cd "$HERMES_HOME" || exit 1
    tar -cf - \
      --exclude=node_modules \
      --exclude=.git \
      --exclude=.venv \
      --exclude=__pycache__ \
      --exclude=dist \
      --exclude=build \
      --exclude="*.pyc" \
      --exclude="*.log" \
      "$rel" 2>/dev/null
  ) | (
    cd "$ROOT" || exit 1
    tar -xf -
  )
  echo "  + $rel (filtered)"
}

run_with_timeout() {
  # A locked SQLite file on a network/9p mount can block forever; cap each dump.
  if command -v timeout >/dev/null 2>&1; then
    timeout 20 "$@"
  else
    "$@"
  fi
}

backup_sqlite() {
  local name="$1"
  [ -f "$HERMES_HOME/$name" ] || return 0
  # Write to a temp file outside the backup tree: a failed dump must not leave a
  # 0-byte <name>.db behind, which restore would happily install.
  local tmp
  tmp="$(mktemp 2>/dev/null || echo "$DEST/.partial-$name")"
  if run_with_timeout "$PY" - "$HERMES_HOME/$name" "$tmp" <<'PY'
import sqlite3, sys
src, dst = sys.argv[1], sys.argv[2]
try:
    s = sqlite3.connect("file:%s?mode=ro" % src, uri=True, timeout=2)
except Exception:
    s = sqlite3.connect(src, timeout=2)   # UNC / Windows paths break the URI form
d = sqlite3.connect(dst)
with d:
    s.backup(d)
s.close(); d.close()
PY
  then
    mv -f "$tmp" "$ROOT/$name"
    echo "  ~ $name (sqlite online backup)"
  else
    echo "  ! $name backup failed (locked or unreachable?) — run inside WSL for the state tier"
  fi
}

backup_mem0_service() {
  local dir="$MEM0_SERVICE_DIR" out="$DEST/mem0-service"
  if [ ! -f "$dir/docker-compose.yaml" ]; then
    echo "  - mem0 service not found at $dir (skipped; override with MEM0_SERVICE_DIR)"
    return 0
  fi
  mkdir -p "$out"
  cp "$dir/docker-compose.yaml" "$out/" 2>/dev/null || true
  if [ -f "$dir/.env" ]; then
    {
      echo "# mem0 service env — keys only, fill values before 'docker compose up'"
      awk '/^[A-Za-z_][A-Za-z0-9_]*=/ {split($0,a,"="); print a[1]"="}' "$dir/.env"
    } > "$out/.env.example"
  fi
  if ! command -v docker >/dev/null 2>&1; then
    echo "  ! docker not available — compose saved, containers/db not dumped"
    return 0
  fi
  docker ps --filter name=mem0 --format '{{.Names}}\t{{.Image}}\t{{.Status}}' > "$out/containers.txt" 2>/dev/null || true
  local ctr db pg_user
  ctr="$(docker ps --format '{{.Names}}' 2>/dev/null | grep -E 'mem0.*postgres|postgres.*mem0' | head -1)"
  db="$(grep -E '^APP_DB_NAME=' "$dir/.env" 2>/dev/null | cut -d= -f2 | tr -d '\r')"
  pg_user="$(grep -E '^POSTGRES_USER=' "$dir/.env" 2>/dev/null | cut -d= -f2 | tr -d '\r')"
  [ -n "$db" ] || db="mem0_app"
  [ -n "$pg_user" ] || pg_user="postgres"
  if [ -n "$ctr" ] && docker exec "$ctr" pg_dump -U "$pg_user" -d "$db" 2>/dev/null > "$out/$db.sql"; then
    gzip -f "$out/$db.sql" 2>/dev/null || true
    echo "  + mem0-service/$db.sql.gz"
  else
    echo "  ! pg_dump skipped (container not running?) — compose + env keys still saved"
  fi
  echo "  + mem0-service/ (compose, env keys, containers.txt)"
}

echo "[1/4] source: $HERMES_HOME"
echo "      tier:   $TIER"
echo "      dest:   $DEST"

echo "[2/4] copying files"
for item in "${CONFIG_ITEMS[@]}"; do copy_path "$item"; done

if [ -d "$HERMES_HOME/plugins" ]; then
  if [ "$WITH_PLUGINS" = "1" ]; then
    copy_tree_filtered plugins
  else
    printf '# plugin\tsha\torigin\n' > "$DEST/plugins.txt"
    for d in "$HERMES_HOME"/plugins/*/; do
      [ -d "$d" ] || continue
      name="$(basename "$d")"
      if [ -d "$d/.git" ]; then
        sha="$(git -C "$d" rev-parse --short HEAD 2>/dev/null || echo '-')"
        url="$(git -C "$d" remote get-url origin 2>/dev/null || echo '-')"
      elif [ "$name" = "mem0" ]; then
        sha="-"
        url="(not a git repo; code copied into files/hermes/plugins/mem0)"
      else
        sha="-"
        url="(not a git repo; re-run with --with-plugins to copy the code)"
      fi
      printf '%s\t%s\t%s\n' "$name" "$sha" "$url" >> "$DEST/plugins.txt"
    done
    echo "  + plugins.txt (code not copied; add --with-plugins to include it)"
  fi
fi

# mem0 plugin is not a git repo (cannot be rebuilt from a sha) and is small:
# always copy it, even when other plugin code is left out.
if [ -d "$HERMES_HOME/plugins/mem0" ] && [ "$WITH_PLUGINS" != "1" ]; then
  copy_path plugins/mem0
fi

if [ "$WITH_MEM0_SERVICE" = "1" ]; then
  backup_mem0_service
fi

if [ "$TIER" != "config" ]; then
  for item in "${STATE_ITEMS[@]}"; do copy_path "$item"; done
  for item in "${DB_ITEMS[@]}";   do backup_sqlite "$item"; done
fi

if [ "$TIER" = "full" ]; then
  for item in "${FULL_ITEMS[@]}"; do copy_tree_filtered "$item"; done
fi

if [ -f "$HERMES_HOME/.env" ]; then
  {
    echo "# Hermes .env template — VALUES ARE NOT INCLUDED (secrets are never exported)."
    echo "# Fill every key below before starting Hermes."
    awk '/^[A-Za-z_][A-Za-z0-9_]*=/ {split($0,a,"="); print a[1]"="}' "$HERMES_HOME/.env"
  } > "$ROOT/.env.example"
  echo "  + .env.example (keys only)"
fi

if [ -d "$HERMES_HOME/skills" ]; then
  links="$(find "$HERMES_HOME/skills" -type l 2>/dev/null || true)"
  if [ -n "$links" ]; then
    printf '%s\n' "$links" > "$DEST/symlinks.txt"
    echo "  ! symlinks recorded in symlinks.txt (fix them after restore)"
  fi
fi

echo "[3/4] writing manifest"

"$PY" - "$DEST" "$TIER" "$HERMES_HOME" <<'PY'
import json, os, sys, datetime, subprocess

dest, tier, home = sys.argv[1], sys.argv[2], sys.argv[3]
files = []
for base, _dirs, names in os.walk(os.path.join(dest, "files")):
    for n in names:
        p = os.path.join(base, n)
        try:
            files.append({"path": os.path.relpath(p, dest).replace("\\", "/"),
                          "size": os.path.getsize(p)})
        except OSError:
            pass

def version():
    exe = os.path.join(home, "hermes-agent", ".venv", "bin", "hermes")
    for cmd in ([exe] if os.path.exists(exe) else []) + ["hermes"]:
        try:
            out = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=20)
            if out.returncode == 0 and out.stdout.strip():
                return out.stdout.strip().splitlines()[0]
        except Exception:
            continue
    return "unknown"

manifest = {
    "tool": "hermes-portability",
    "created_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    "tier": tier,
    "source_home": home,
    "host": os.uname().nodename if hasattr(os, "uname") else "windows",
    "hermes_version": version(),
    "mem0_service": os.path.isdir(os.path.join(dest, "mem0-service")),
    "file_count": len(files),
    "total_bytes": sum(f["size"] for f in files),
    "files": files,
}
with open(os.path.join(dest, "manifest.json"), "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, ensure_ascii=False, indent=2)
print("  + manifest.json (%d files, %.1f MB)" % (manifest["file_count"], manifest["total_bytes"] / 1048576))
PY

echo "[4/4] writing RESTORE.md"
{
  echo "# 恢复步骤（$TIER 层，生成于 $STAMP）"
  echo
  echo "1. 目标机器先装 Hermes："
  echo '   `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`'
  echo
  echo "2. 还原文件："
  echo "   \`bash restore.sh --from \"$DEST\" --to ~/.hermes --force\`"
  echo
  echo "3. 补密钥："
  echo '   `cp ~/.hermes/.env.example ~/.hermes/.env`，然后逐个填值。'
  echo "   auth.json 不在备份内，需要重新登录（\`hermes auth --help\`）。"
  echo
  if [ "$TIER" = "full" ]; then
    echo "4. 重建依赖（full 层）："
    echo '   `cd ~/.hermes/hermes-agent && .venv/bin/pip install -e .`'
    echo
  fi
  echo "5. 体检："
  echo '   `bash verify.sh`'
  if [ -d "$DEST/mem0-service" ]; then
    echo
    echo "6. mem0 服务（独立 Docker 栈，恢复完 Hermes 后再做）："
    echo '   `cd ~/mem0/server && cp /path/to/mem0-service/.env.example .env`，填值'
    echo '   `docker compose up -d`'
    echo '   `gunzip -c /path/to/mem0-service/mem0_app.sql.gz | docker exec -i $(docker ps --format "{{.Names}}" | grep -E "mem0.*postgres" | head -1) psql -U postgres -d mem0_app`'
  fi
} > "$DEST/RESTORE.md"

SIZE="$(du -sh "$DEST" 2>/dev/null | cut -f1 || echo '?')"
echo
echo "done: $DEST  ($SIZE)"
echo "next: read $DEST/RESTORE.md"
