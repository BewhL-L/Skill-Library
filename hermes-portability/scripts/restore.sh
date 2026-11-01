#!/usr/bin/env bash
# Restore a Hermes backup created by export.sh.
#
# Usage:
#   bash restore.sh --from BACKUP_DIR [--to ~/.hermes] [--force | --merge]
#
# --force  rename the existing target to <target>.bak.<timestamp>, then restore clean
# --merge  overlay onto the existing target (keeps .venv / installs / tools)
# Without either flag a non-empty target is refused.
set -euo pipefail

FROM=""
TO="${HERMES_HOME:-$HOME/.hermes}"
FORCE=0
MERGE=0

usage() { sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0; }

while [ $# -gt 0 ]; do
  case "$1" in
    --from)  FROM="${2:-}"; shift 2 ;;
    --to)    TO="${2:-}";   shift 2 ;;
    --force) FORCE=1;       shift ;;
    --merge) MERGE=1;       shift ;;
    -h|--help) usage ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

[ -n "$FROM" ] || { echo "--from is required" >&2; exit 2; }
if [ "$FORCE" = "1" ] && [ "$MERGE" = "1" ]; then
  echo "--force and --merge are mutually exclusive" >&2
  exit 2
fi
[ -f "$FROM/manifest.json" ] || { echo "not a backup dir (manifest.json missing): $FROM" >&2; exit 1; }
[ -d "$FROM/files/hermes" ] || { echo "payload missing: $FROM/files/hermes" >&2; exit 1; }

TIER="$(grep -o '"tier"[^,]*' "$FROM/manifest.json" | head -1 | sed 's/.*"tier"[[:space:]]*:[[:space:]]*"//; s/"//')"
echo "backup: $FROM"
echo "tier:   ${TIER:-unknown}"
echo "target: $TO"

if [ "$MERGE" = "1" ]; then
  # Overlay onto an existing install (typical after the official installer ran):
  # keep .venv / installs / tools created by the installer, replace only the
  # files present in the backup.
  mkdir -p "$TO"
  echo "merge mode: existing files are kept unless the backup has a replacement"
elif [ -d "$TO" ] && [ -n "$(ls -A "$TO" 2>/dev/null || true)" ]; then
  if [ "$FORCE" != "1" ]; then
    echo
    echo "target exists and is not empty. Re-run with --force to replace it" >&2
    echo "(the current directory will be renamed, not deleted)." >&2
    exit 1
  fi
  BAK="$TO.bak.$(date +%Y%m%d-%H%M%S)"
  mv "$TO" "$BAK"
  echo "existing moved to: $BAK"
fi

mkdir -p "$TO"
cp -a "$FROM/files/hermes/." "$TO/"
echo "files restored"

if [ ! -f "$TO/.env" ] && [ -f "$TO/.env.example" ]; then
  cp "$TO/.env.example" "$TO/.env"
  echo
  echo "!! .env was NOT in the backup. Created from .env.example — fill every key before starting:"
  grep -E '^[A-Za-z_][A-Za-z0-9_]*=' "$TO/.env" | sed 's/=$/  <-- TODO/'
fi

if [ -f "$FROM/symlinks.txt" ]; then
  echo
  echo "!! these were symlinks in the source and may be broken now:"
  sed 's/^/   /' "$FROM/symlinks.txt"
fi

VERIFY="$(cd "$(dirname "$0")" && pwd)/verify.sh"
STEP=1

echo
echo "next steps"
echo "  $STEP) secrets:  edit $TO/.env  (auth.json is never backed up — log in again: hermes auth --help)"
STEP=$((STEP + 1))

if [ "$TIER" = "full" ]; then
  echo "  $STEP) deps:     cd $TO/hermes-agent && .venv/bin/pip install -e ."
  echo "                  (or re-run the official installer to repair the environment)"
  STEP=$((STEP + 1))
fi

echo "  $STEP) verify:   bash \"$VERIFY\""
STEP=$((STEP + 1))
echo "  $STEP) start:    hermes gateway restart   # or: hermes  (interactive)"

if [ -d "$FROM/mem0-service" ]; then
  STEP=$((STEP + 1))
  echo "  $STEP) mem0 服务（独立 Docker 栈）："
  echo "                  cd ~/mem0/server && cp \"$FROM/mem0-service/.env.example\" .env  # 填值"
  echo "                  docker compose up -d"
  echo "                  gunzip -c \"$FROM/mem0-service/mem0_app.sql.gz\" | docker exec -i \\"
  echo "                    \$(docker ps --format '{{.Names}}' | grep -E 'mem0.*postgres' | head -1) \\"
  echo "                    psql -U postgres -d mem0_app"
fi
