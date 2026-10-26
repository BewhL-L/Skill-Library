#!/bin/bash

# ============================================================
#   Obsidian 知识库工具 - macOS/Linux 安装脚本
# ============================================================

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================================"
echo "  📦 Obsidian 知识库工具 - 安装脚本"
echo "============================================================"
echo ""
echo "📁 工具目录: $SCRIPT_DIR"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python 3.7+"
    echo "   下载地址: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python3 已安装"
python3 --version
echo ""

# 检查 kb.py 是否存在
if [ ! -f "$SCRIPT_DIR/scripts/kb.py" ]; then
    echo "❌ 找不到 kb.py，请确认在正确的目录下运行"
    exit 1
fi

echo "✅ kb.py 存在"
echo ""

# 检查是否已经在 PATH 中
if echo "$PATH" | grep -q "$SCRIPT_DIR"; then
    echo "✅ 工具目录已在系统 PATH 中"
    echo ""
    echo "🎉 安装完成！"
    echo ""
    echo "使用方法:"
    echo "  kb init --name \"我的知识库\" --path ./my-kb"
    echo "  kb note --title \"Vue3\" --category 前端开发 --kb-root ./my-kb"
    echo "  kb standardize --kb-root ./my-kb"
    echo "  kb info"
    echo ""
    exit 0
fi

# 询问安装方式
echo "⚠️  工具目录不在系统 PATH 中"
echo ""
echo "选择安装方式:"
echo "  [1] 添加到用户 PATH（推荐，仅当前用户）"
echo "  [2] 添加到系统 PATH（所有用户，需要 sudo 权限）"
echo "  [3] 创建命令别名（仅当前 shell 配置文件）"
echo "  [4] 取消安装"
echo ""
read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "📝 正在添加到用户 PATH..."
        echo ""

        # 确定 shell 配置文件
        if [ -n "$ZSH_VERSION" ] || [ "$SHELL" = "/bin/zsh" ]; then
            PROFILE_FILE="$HOME/.zshrc"
        else
            PROFILE_FILE="$HOME/.bashrc"
        fi

        # 检查是否已经添加过
        if grep -q "obsidian-knowledge-base-creator" "$PROFILE_FILE" 2>/dev/null; then
            echo "⚠️  已存在于 $PROFILE_FILE"
        else
            echo "" >> "$PROFILE_FILE"
            echo "# Obsidian 知识库工具" >> "$PROFILE_FILE"
            echo "export PATH=\"$SCRIPT_DIR:\$PATH\"" >> "$PROFILE_FILE"
            echo "alias kb='python3 \"$SCRIPT_DIR/scripts/kb.py\"'" >> "$PROFILE_FILE"
            echo "✅ 已添加到 $PROFILE_FILE"
        fi

        echo ""
        echo "💡 请运行以下命令使配置生效，或重新打开终端:"
        echo "  source $PROFILE_FILE"
        ;;

    2)
        echo ""
        echo "📝 正在添加到系统 PATH..."
        echo ""

        # 检查是否有 sudo 权限
        if ! sudo -n true 2>/dev/null; then
            echo "⚠️  需要 sudo 权限，请输入密码..."
        fi

        # 创建符号链接到 /usr/local/bin
        sudo ln -sf "$SCRIPT_DIR/scripts/kb.py" /usr/local/bin/kb
        sudo chmod +x /usr/local/bin/kb

        # 创建包装脚本
        cat > /tmp/kb-wrapper << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
python3 "$SCRIPT_DIR/scripts/kb.py" "$@"
EOF
        sudo mv /tmp/kb-wrapper /usr/local/bin/kb
        sudo chmod +x /usr/local/bin/kb

        echo "✅ 已创建命令链接: /usr/local/bin/kb"
        ;;

    3)
        echo ""
        echo "📝 正在创建命令别名..."
        echo ""

        # 确定 shell 配置文件
        if [ -n "$ZSH_VERSION" ] || [ "$SHELL" = "/bin/zsh" ]; then
            PROFILE_FILE="$HOME/.zshrc"
        else
            PROFILE_FILE="$HOME/.bashrc"
        fi

        # 检查是否已经添加过
        if grep -q "alias kb=" "$PROFILE_FILE" 2>/dev/null; then
            echo "⚠️  别名已存在于 $PROFILE_FILE"
        else
            echo "" >> "$PROFILE_FILE"
            echo "# Obsidian 知识库工具" >> "$PROFILE_FILE"
            echo "alias kb='python3 \"$SCRIPT_DIR/scripts/kb.py\"'" >> "$PROFILE_FILE"
            echo "✅ 已添加别名到 $PROFILE_FILE"
        fi

        echo ""
        echo "💡 请运行以下命令使配置生效，或重新打开终端:"
        echo "  source $PROFILE_FILE"
        ;;

    4)
        echo ""
        echo "❌ 安装已取消"
        exit 0
        ;;

    *)
        echo ""
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "============================================================"
echo "  🎉 安装完成！"
echo "============================================================"
echo ""
echo "📁 工具目录: $SCRIPT_DIR"
echo ""
echo "💡 使用方法（新开一个终端窗口生效）:"
echo ""
echo "  初始化知识库:"
echo "    kb init --name \"我的知识库\" --path ./my-kb"
echo ""
echo "  生成笔记:"
echo "    kb note --title \"Vue3\" --category 前端开发 --kb-root ./my-kb"
echo ""
echo "  批量生成笔记:"
echo "    kb batch-note --list notes.json --kb-root ./my-kb"
echo ""
echo "  一键标准化:"
echo "    kb standardize --kb-root ./my-kb"
echo ""
echo "  查看学习进度:"
echo "    kb progress --kb-root ./my-kb"
echo ""
echo "  查看帮助:"
echo "    kb info"
echo ""
echo "⚠️  注意: 修改 PATH 后需要重新打开终端窗口才能生效"
echo ""
