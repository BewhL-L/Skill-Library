@echo off
chcp 65001 >nul
REM ============================================
REM Obsidian 知识库标准化工具 - 一键安装脚本
REM 用法: install.bat
REM 功能: 检测Python环境、安装依赖、验证安装
REM ============================================

setlocal enabledelayedexpansion

echo.
echo ============================================
echo   Obsidian 知识库标准化工具 - 安装向导
echo ============================================
echo.

REM ===== 1. 检测 Python 环境 =====
echo [1/4] 检测 Python 环境...
where python >nul 2>nul
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.7+
    echo.
    echo 下载地址: https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo [OK] Python 版本: %PY_VER%

REM 检查 Python 版本是否 >= 3.7
for /f "tokens=1,2 delims=." %%a in ("%PY_VER%") do (
    set PY_MAJOR=%%a
    set PY_MINOR=%%b
)
if %PY_MAJOR% LSS 3 (
    echo [错误] Python 版本过低，需要 3.7+，当前: %PY_VER%
    pause
    exit /b 1
)
if %PY_MAJOR% EQU 3 if %PY_MINOR% LSS 7 (
    echo [错误] Python 版本过低，需要 3.7+，当前: %PY_VER%
    pause
    exit /b 1
)

REM ===== 2. 安装依赖 =====
echo.
echo [2/4] 安装 Python 依赖...

REM 安装 PyYAML（配置文件功能需要）
python -c "import yaml" >nul 2>nul
if errorlevel 1 (
    echo   安装 PyYAML...
    pip install pyyaml -q
    if errorlevel 1 (
        echo [警告] PyYAML 安装失败，配置文件功能将不可用
        echo        请手动运行: pip install pyyaml
    ) else (
        echo [OK] PyYAML 安装成功
    )
) else (
    echo [OK] PyYAML 已安装
)

REM ===== 3. 验证脚本文件 =====
echo.
echo [3/4] 验证脚本文件...

set SCRIPT_DIR=%~dp0
set ERROR_COUNT=0

if not exist "%SCRIPT_DIR%scripts\kb.py" (
    echo [错误] 缺少 scripts/kb.py
    set /a ERROR_COUNT+=1
)
if not exist "%SCRIPT_DIR%scripts\init-kb.py" (
    echo [错误] 缺少 scripts/init-kb.py
    set /a ERROR_COUNT+=1
)
if not exist "%SCRIPT_DIR%scripts\generate-note.py" (
    echo [错误] 缺少 scripts/generate-note.py
    set /a ERROR_COUNT+=1
)
if not exist "%SCRIPT_DIR%scripts\generate-moc.py" (
    echo [错误] 缺少 scripts/generate-moc.py
    set /a ERROR_COUNT+=1
)
if not exist "%SCRIPT_DIR%scripts\config.py" (
    echo [错误] 缺少 scripts/config.py
    set /a ERROR_COUNT+=1
)
if not exist "%SCRIPT_DIR%assets\note-template.md" (
    echo [错误] 缺少 assets/note-template.md
    set /a ERROR_COUNT+=1
)

if %ERROR_COUNT% GTR 0 (
    echo [错误] 缺少 %ERROR_COUNT% 个文件，请重新下载完整工具包
    pause
    exit /b 1
)
echo [OK] 所有脚本文件完整

REM ===== 4. 验证功能 =====
echo.
echo [4/4] 验证核心功能...

REM 验证 config.py
python -c "import sys; sys.path.insert(0, r'%SCRIPT_DIR%scripts'); from config import load_config, get_categories; c = load_config(); cats = get_categories(c); print(f'  配置模块: OK ({len(cats)} 个分类)')" 2>nul
if errorlevel 1 (
    echo [警告] 配置模块验证失败
)

REM 验证 init-kb.py 语法
python -m py_compile "%SCRIPT_DIR%scripts\init-kb.py" 2>nul
if errorlevel 1 (
    echo [警告] init-kb.py 语法错误
) else (
    echo   init-kb.py: OK
)

REM 验证 generate-note.py 语法
python -m py_compile "%SCRIPT_DIR%scripts\generate-note.py" 2>nul
if errorlevel 1 (
    echo [警告] generate-note.py 语法错误
) else (
    echo   generate-note.py: OK
)

echo.
echo ============================================
echo   安装完成！
echo ============================================
echo.
echo 快速开始:
echo   1. 生成演示知识库（含示例笔记）:
echo      kb.bat init --name "演示库" --path ./demo --demo
echo.
echo   2. 生成空知识库:
echo      kb.bat init --name "我的知识库" --path ./my-kb
echo.
echo   3. 生成标准化笔记:
echo      kb.bat note --title "Vue3响应式原理" --category 前端开发 --kb-root ./my-kb
echo.
echo   4. 查看帮助:
echo      kb.bat info
echo.
echo 更多信息请查看 QUICKSTART.md 和 SKILL.md
echo.
pause
endlocal
