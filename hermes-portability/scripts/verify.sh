#!/usr/bin/env bash
# Read-only health check for a Hermes installation.
#
# Usage:
#   bash verify.sh [--home ~/.hermes]
#
# Exit code: 0 = no FAIL, 1 = at least one FAIL.
set -uo pipefail

HOME_DIR="${HERMES_HOME:-$HOME/.hermes}"
while [ $# -gt 0 ]; do
  case "$1" in
    --home) HOME_DIR="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

PY="$(command -v python3 || command -v python || true)"
FAILS=0
WARNS=0

ok()   { printf '  OK    %s\n' "$1"; }
warn() { printf '  WARN  %s\n' "$1"; WARNS=$((WARNS+1)); }
fail() { printf '  FAIL  %s\n' "$1"; FAILS=$((FAILS+1)); }

echo "hermes home: $HOME_DIR"
echo

# 1. home
if [ -d "$HOME_DIR" ]; then ok "directory exists"; else fail "directory missing — restore a backup or run the installer"; fi

# 2. config
if [ -f "$HOME_DIR/config.yaml" ]; then
  if grep -q '^agent:' "$HOME_DIR/config.yaml"; then ok "config.yaml parses (has 'agent')"
  else warn "config.yaml exists but no top-level 'agent' key — check for truncation"; fi
else
  fail "config.yaml missing"
fi

# 3. env + keys
if [ -f "$HOME_DIR/.env" ]; then
  ok ".env present"
  if [ -f "$HOME_DIR/.env.example" ]; then
    missing="$(grep -E '^[A-Za-z_][A-Za-z0-9_]*=' "$HOME_DIR/.env.example" | cut -d= -f1 | while read -r k; do
      grep -qE "^${k}=" "$HOME_DIR/.env" || echo "$k"
    done)"
    if [ -n "$missing" ]; then
      warn "keys declared in .env.example but absent in .env:"
      echo "$missing" | sed 's/^/          /'
    else
      ok "all keys from .env.example are present"
    fi
  fi
  empty="$(grep -E '^[A-Za-z_][A-Za-z0-9_]*=$' "$HOME_DIR/.env" | cut -d= -f1 || true)"
  if [ -n "$empty" ]; then
    warn "keys with empty value (fill them): $(echo "$empty" | tr '\n' ' ')"
  fi
else
  warn ".env missing — copy .env.example and fill the keys"
fi

# 4. auth
if [ -f "$HOME_DIR/auth.json" ]; then ok "auth.json present"; else warn "auth.json missing — log in again (hermes auth --help)"; fi

# 5. command
if command -v hermes >/dev/null 2>&1; then
  ok "hermes on PATH: $(hermes --version 2>/dev/null | head -1)"
elif [ -x "$HOME_DIR/hermes-agent/.venv/bin/hermes" ]; then
  warn "hermes not on PATH; found at $HOME_DIR/hermes-agent/.venv/bin/hermes"
else
  fail "hermes executable not found — run the official installer"
fi

# 6. databases
for db in state.db kanban.db shared-state.db; do
  [ -f "$HOME_DIR/$db" ] || continue
  if [ -z "$PY" ]; then warn "$db found, cannot check (python3 missing)"; continue; fi
  res="$("$PY" - "$HOME_DIR/$db" <<'PY' 2>&1
import sqlite3, sys
p = sys.argv[1]
try:
    try:
        con = sqlite3.connect("file:%s?mode=ro" % p, uri=True)
    except Exception:
        con = sqlite3.connect(p)          # UNC / Windows paths break the URI form
    con.execute("PRAGMA busy_timeout=2000")
    print(con.execute("PRAGMA quick_check").fetchone()[0])
except Exception as exc:
    msg = str(exc)
    print("locked" if "locked" in msg.lower() else "error: %s" % msg)
PY
)"
  if [ "$res" = "ok" ]; then
    ok "$db integrity ok"
  elif [ "$res" = "locked" ]; then
    warn "$db is locked (Hermes is running) — integrity not checked"
  else
    fail "$db integrity: $res"
  fi
done

# 7. gateway
if [ -f "$HOME_DIR/gateway_state.json" ]; then
  state="$(grep -o '"gateway_state"[^,]*' "$HOME_DIR/gateway_state.json" | head -1 | sed 's/.*: *"//; s/"//')"
  ok "gateway_state.json present (state=${state:-unknown})"
else
  warn "gateway_state.json missing — gateway has never started on this install"
fi

# 8. custom assets
for d in skills hooks desktop-plugins; do
  if [ -d "$HOME_DIR/$d" ]; then
    n="$(find "$HOME_DIR/$d" -mindepth 1 -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')"
    ok "$d/ present ($n entries)"
  else
    warn "$d/ missing (fine on a fresh install)"
  fi
done

# 9. enabled plugins vs installed plugin code
if [ -f "$HOME_DIR/config.yaml" ]; then
  enabled="$(awk '
    /^plugins:/ {inb=1; next}
    inb && /^[^[:space:]]/ {inb=0}
    inb && /^[[:space:]]+-[[:space:]]+/ {gsub(/^[[:space:]]+-[[:space:]]+/,""); print}
  ' "$HOME_DIR/config.yaml" | sed 's#/.*##' | sort -u)"
  if [ -n "$enabled" ]; then
    missing=""
    for p in $enabled; do
      if [ ! -e "$HOME_DIR/plugins/$p" ] && [ ! -e "$HOME_DIR/hermes-agent/plugins/$p" ]; then
        missing="$missing $p"
      fi
    done
    if [ -n "$missing" ]; then
      warn "enabled in config.yaml but not installed:$missing"
      echo "          (restore ~/.hermes/plugins/ from the backup, or disable them in config.yaml)"
    else
      ok "all enabled plugins found"
    fi
  fi
fi

echo
echo "summary: $FAILS fail, $WARNS warn"
[ "$FAILS" -eq 0 ] || exit 1
