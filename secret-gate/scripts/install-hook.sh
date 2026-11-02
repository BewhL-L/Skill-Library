#!/usr/bin/env bash
# 给指定仓库安装 pre-commit 闸门。
# 用法：bash install-hook.sh [仓库根，默认当前目录]
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GATE="$SKILL_DIR/scripts/gate.py"
REPO="${1:-.}"

if [ ! -d "$REPO/.git" ]; then
    echo "install-hook: $REPO 不是 git 仓库" >&2
    exit 1
fi
if [ ! -f "$GATE" ]; then
    echo "install-hook: 找不到 $GATE" >&2
    exit 1
fi

HOOK="$REPO/.git/hooks/pre-commit"
if [ -f "$HOOK" ] && ! grep -q "gate.py" "$HOOK"; then
    cp "$HOOK" "$HOOK.bak.$(date +%Y%m%d-%H%M%S)"
    echo "已备份原有 pre-commit"
fi

cat > "$HOOK" <<EOF
#!/usr/bin/env bash
# 由 secret-gate 技能安装；删除本文件即可卸载。
exec python "$GATE" "\$(git rev-parse --show-toplevel)" --staged
EOF

chmod +x "$HOOK"
echo "installed: $HOOK"
echo "卸载：rm '$HOOK'"
