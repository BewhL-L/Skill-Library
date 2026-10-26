@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================================
echo   🗑️  Obsidian 知识库工具 - 卸载脚本
echo ============================================================
echo.

:: 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo 📁 工具目录: %SCRIPT_DIR%
echo.

:: 询问是否确认卸载
set /p confirm=确认要卸载吗？这将从 PATH 中移除工具目录 (y/N): 
if /i not "%confirm%"=="y" (
    echo ❌ 卸载已取消
    pause
    exit /b 0
)

echo.
echo 📝 正在卸载...
echo.

:: 从用户 PATH 中移除
echo 正在从用户 PATH 中移除...
powershell -Command "$current = [Environment]::GetEnvironmentVariable('Path', 'User'); $newPath = ($current -split ';' | Where-Object { $_ -ne '%SCRIPT_DIR%' -and $_ -ne '' }) -join ';'; [Environment]::SetEnvironmentVariable('Path', $newPath, 'User'); Write-Host '✅ 已从用户 PATH 移除'"

:: 从系统 PATH 中移除（需要管理员权限）
echo.
echo 正在检查系统 PATH...
net session >nul 2>&1
if %errorlevel% equ 0 (
    powershell -Command "$current = [Environment]::GetEnvironmentVariable('Path', 'Machine'); $newPath = ($current -split ';' | Where-Object { $_ -ne '%SCRIPT_DIR%' -and $_ -ne '' }) -join ';'; [Environment]::SetEnvironmentVariable('Path', $newPath, 'Machine'); Write-Host '✅ 已从系统 PATH 移除'"
) else (
    echo ⚠️  非管理员权限，跳过系统 PATH 清理
    echo    如需清理系统 PATH，请以管理员身份运行此脚本
)

:: 检查桌面快捷方式
echo.
echo 正在检查桌面快捷方式...
set "SHORTCUT=%USERPROFILE%\Desktop\知识库工具.lnk"
if exist "%SHORTCUT%" (
    del "%SHORTCUT%"
    echo ✅ 已删除桌面快捷方式
) else (
    echo ℹ️  未找到桌面快捷方式
)

echo.
echo ============================================================
echo   ✅ 卸载完成！
echo ============================================================
echo.
echo 📝 说明:
echo   - 工具文件未被删除，仅从 PATH 中移除
echo   - 如需完全删除，请手动删除工具目录
echo   - 重新打开终端窗口后生效
echo.
echo 📁 工具目录: %SCRIPT_DIR%
echo.
pause
exit /b 0
