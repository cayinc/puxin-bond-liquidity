@echo off
chcp 65001 >nul 2>&1
title 普信债数据 - 一键更新

echo ==========================================
echo   普信债流动性数据 一键更新
echo ==========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查是否有变更...
git add -A
set changes=
for /f %%i in ('git status --porcelain') do set changes=%%i

if "%changes%"=="" (
    echo ✓ 没有需要更新的文件，退出。
    timeout /t 3 >nul
    exit /b
)

echo.
echo [2/3] 提交并推送...
git commit -m "更新数据 %date% %time:~0,5%"
if %errorlevel% neq 0 (
    echo ✗ 提交失败，请检查是否有冲突。
    pause
    exit /b 1
)

git push origin main
if %errorlevel% neq 0 (
    echo ✗ 推送失败，请检查网络连接。
    pause
    exit /b 1
)

echo.
echo [3/3] 推送成功！
echo.
echo   网站将在 2-3 分钟内自动更新。
echo   访问: https://cayinc.github.io/puxin-bond-liquidity/
echo.
timeout /t 5 >nul
