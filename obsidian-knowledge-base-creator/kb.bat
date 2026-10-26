@echo off
chcp 65001 >nul
REM ============================================
REM Obsidian 知识库标准化工具 - Windows 快捷脚本 (v2.0)
REM 用法: kb.bat <命令> [参数]
REM 示例:
REM   kb.bat init --name "我的知识库" --path ./my-kb
REM   kb.bat init --name "演示库" --path ./demo --demo
REM   kb.bat note --title "Vue3" --category 前端开发 --kb-root ./my-kb
REM   kb.bat audit --kb-root ./my-kb
REM ============================================

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set PYTHON_SCRIPT=%SCRIPT_DIR%scripts\kb.py

REM ===== 环境检测 =====
where python >nul 2>nul
if errorlevel 1 (
    echo.
    echo [错误] 未检测到 Python，请先安装 Python 3.7+
    echo.
    echo 下载地址: https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM 检查 Python 版本
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo [信息] Python 版本: %PY_VER%

REM 检查 kb.py 是否存在
if not exist "%PYTHON_SCRIPT%" (
    echo [错误] 未找到 kb.py: %PYTHON_SCRIPT%
    echo 请确认脚本文件完整
    pause
    exit /b 1
)

REM 检查 PyYAML 依赖（配置功能需要）
python -c "import yaml" >nul 2>nul
if errorlevel 1 (
    echo [警告] 未安装 PyYAML，配置文件功能将不可用
    echo        运行: pip install pyyaml
    echo.
)

REM ===== 无参数时显示帮助 =====
if "%~1"=="" (
    echo.
    echo ============================================
    echo   Obsidian 知识库标准化工具 v2.0
    echo ============================================
    echo.
    echo 常用命令:
    echo   init      初始化知识库（12分类目录 + Home + MOC + 学习路线）
    echo   note      生成单篇标准化笔记（自动更新MOC）
    echo   batch-note 从 JSON 列表批量生成笔记
    echo   moc       生成/更新 MOC 内容地图
    echo   audit     健康检查（Frontmatter/标签/死链/孤立文档/MOC）
    echo   validate  质量校验（五段式结构/排版/代码块/链接）
    echo   standardize 一键标准化（补全Frontmatter + 修复死链 + 生成MOC）
    echo   progress  生成学习进度报告
    echo   info      显示帮助信息
    echo.
    echo 示例:
    echo   kb.bat init --name "我的知识库" --path ./my-kb
    echo   kb.bat init --name "演示库" --path ./demo --demo
    echo   kb.bat init --name "AI库" --path ./ai-kb --config themes/ai-engineering.yaml
    echo   kb.bat note --title "Vue3响应式原理" --category 前端开发 --kb-root ./my-kb
    echo   kb.bat audit --kb-root ./my-kb
    echo.
    echo 更多帮助: kb.bat info
    echo.
    goto :eof
)

REM ===== 执行命令 =====
python "%PYTHON_SCRIPT%" %*

REM ===== 错误处理 =====
if errorlevel 1 (
    echo.
    echo [错误] 命令执行失败，退出码: %errorlevel%
    echo.
    echo 排查建议:
    echo   1. 检查参数是否正确，使用 kb.bat info 查看帮助
    echo   2. 检查路径是否正确，目录是否有写入权限
    echo   3. 检查 Python 版本是否为 3.7+
    echo   4. 查看 FAQ.md 了解常见问题
    echo.
    exit /b %errorlevel%
)

endlocal
