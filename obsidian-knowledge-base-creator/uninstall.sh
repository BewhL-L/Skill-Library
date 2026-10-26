#!/bin/bash

# ============================================================
#   Obsidian 知识库工具 - macOS/Linux 卸载脚本
# ============================================================

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================================"
echo "  🗑️  Obsidian 知识库工具 - 卸载脚本"
echo "============================================================"
echo ""
echo "📁 工具目录: $SCRIPT_DIR"
echo ""

# 询问是否确认卸载
read -p "确认要卸载吗？这将从 PATH 中移除工具目录 (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ 卸载已取消"
    exit 0
fi

echo ""
echo "📝 正在卸载..."
echo ""

# 确定 shell 配置文件
if [ -n "$ZSH_VERSION" ] || [ "$SHELL" = "/bin/zsh" ]; then
    PROFILE_FILE="$HOME/.zshrc"
else
    PROFILE_FILE="$HOME/.bashrc"
fi

# 从 shell 配置文件中移除
echo "正在从 $PROFILE_FILE 中移除..."
if [ -f "$PROFILE_FILE" ]; then
    # 备份原文件
    cp "$PROFILE_FILE" "${PROFILE_FILE}.bak.$(date +%Y%m%d%H%M%S)"

    # 移除相关行
    sed -i '' '/# Obsidian 知识库工具/d' "$PROFILE_FILE" 2>/dev/null || \
    sed -i '/# Obsidian 知识库工具/d' "$PROFILE_FILE" 2>/dev/null || true

    sed -i '' "/obsidian-knowledge-base-creator/d" "$PROFILE_FILE" 2>/dev/null || \
    sed -i '/obsidian-knowledge-base-creator/d' "$PROFILE_FILE" 2>/dev/null || true

    sed -i '' "/alias kb=/d" "$PROFILE_FILE" 2>/dev/null || \
    sed -i '/alias kb=/d' "$PROFILE_FILE" 2>/dev/null || true

    echo "✅ 已从 $PROFILE_FILE 移除"
    echo "   原文件已备份为 ${PROFILE_FILE}.bak.*"
else
    echo "ℹ️  未找到 $PROFILE_FILE"
fi

# 移除 /usr/local/bin 中的符号链接
echo ""
echo "正在检查 /usr/local/bin/kb..."
if [ -L "/usr/local/bin/kb" ] || [ -f "/usr/local/bin/kb" ]; then
    if sudo rm -f /usr/local/bin/kb 2>/dev/null; then
        echo "✅ 已移除 /usr/local/bin/kb"
    else
        echo "⚠️  需要 sudo 权限移除 /usr/local/bin/kb"
        echo "   请手动运行: sudo rm /usr/local/bin/kb"
    fi
else
    echo "ℹ️  未找到 /usr/local/bin/kb"
fi

echo ""
echo "============================================================"
echo "  ✅ 卸载完成！"
echo "============================================================"
echo ""
echo "📝 说明:"
echo "  - 工具文件未被删除，仅从 PATH 中移除"
echo "  - 如需完全删除，请手动删除工具目录"
echo "  - 重新打开终端窗口后生效"
echo "  - shell 配置文件已备份，如需恢复可手动还原"
echo ""
echo "📁 工具目录: $SCRIPT_DIR"
echo ""
