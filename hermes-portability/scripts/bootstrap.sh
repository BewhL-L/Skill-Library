#!/usr/bin/env bash
# One-shot setup on a fresh machine: install Hermes (if missing) -> restore -> verify.
#
# Usage:
#   bash bootstrap.sh --from BACKUP_DIR [--to ~/.hermes] [--yes]
#
#   --from  backup directory produced by export.sh (must contain manifest.json)
#   --to    target install dir (default: $HOME/.hermes or $HERMES_HOME)
#   --yes   allow running the official installer without asking
#
# Without --yes the script stops and prints the install command instead of
# executing a remote script.
set -euo pipefail

FROM=""
TO="${HERMES_HOME:-$HOME/.hermes}"
ASSUME_YES=0
HERE="$(cd "$(dirname "$0")" && pwd)"

usage() { sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0; }

while [ $# -gt 0 ]; do
  case "$1" in
    --from) FROM="${2:-}"; shift 2 ;;
    --to)   TO="${2:-}";   shift 2 ;;
    --yes|-y) ASSUME_YES=1; shift ;;
    -h|--help) usage ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

[ -n "$FROM" ] || { echo "--from is required" >&2; exit 2; }
[ -f "$FROM/manifest.json" ] || { echo "not a backup dir: $FROM" >&2; exit 1; }

echo "== 1/4 环境检查 =="
command -v tar >/dev/null || { echo "tar 缺失" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1 || {
  echo "python3 缺失（SQLite 备份与清单需要）" >&2; exit 1; }

if command -v hermes >/dev/null 2>&1; then
  echo "   hermes 已在 PATH：$(hermes --version 2>/dev/null | head -1)"
elif [ -x "$TO/hermes-agent/.venv/bin/hermes" ]; then
  echo "   hermes 已存在于 $TO/hermes-agent/.venv/bin/hermes"
else
  echo "   hermes 未安装"
  echo
  echo "   官方安装命令："
  echo "     curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash"
  echo
  if [ "$ASSUME_YES" != "1" ]; then
    echo "   确认后重跑：bash $0 --from \"$FROM\" --yes" >&2
    echo "   （脚本不擅自执行远程安装；加 --yes 才会运行上面的命令）" >&2
    exit 1
  fi
  echo "   执行官方安装（--yes 已确认）..."
  set +e
  curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
  INSTALL_RC=${PIPESTATUS[0]}
  set -e
  if [ "$INSTALL_RC" -ne 0 ]; then
    echo "安装脚本返回 $INSTALL_RC，中止。" >&2
    exit 1
  fi
  if [ ! -x "$TO/hermes-agent/.venv/bin/hermes" ] && ! command -v hermes >/dev/null 2>&1; then
    echo "安装完成但找不到 hermes 可执行文件（期望 $TO/hermes-agent/.venv/bin/hermes）。" >&2
    echo "请检查安装日志，或手动执行安装命令后重跑本脚本。" >&2
    exit 1
  fi
  echo "   安装完成"
fi

echo
echo "== 2/4 还原配置与状态 =="
# --merge: the installer just created .venv / installs / tools; keep them and
# only overlay what the backup contains. --force would throw those away.
bash "$HERE/restore.sh" --from "$FROM" --to "$TO" --merge

echo
echo "== 3/4 体检 =="
set +e
bash "$HERE/verify.sh" --home "$TO"
VERIFY_RC=$?
set -e

echo
echo "== 4/4 待办清单 =="
cat <<EOF
  [ ] 填 $TO/.env 里的密钥（verify.sh 会列出缺失项）
  [ ] 重新登录：hermes auth --help
  [ ] 按 $FROM/plugins.txt 重装第三方插件（mem0 已随备份复制）
EOF

if [ -d "$FROM/mem0-service" ]; then
  cat <<EOF
  [ ] 恢复 mem0 Docker 栈：
        cd ~/mem0/server && cp "$FROM/mem0-service/.env.example" .env   # 填值
        docker compose up -d
        gunzip -c "$FROM/mem0-service/mem0_app.sql.gz" | docker exec -i \\
          \$(docker ps --format '{{.Names}}' | grep -E 'mem0.*postgres' | head -1) \\
          psql -U postgres -d mem0_app
EOF
fi

echo
if [ "$VERIFY_RC" -eq 0 ]; then
  echo "环境已就绪（verify 无 FAIL）。"
else
  echo "verify 有 FAIL，按上面提示处理后再跑一次：bash \"$HERE/verify.sh\"" >&2
  exit "$VERIFY_RC"
fi
