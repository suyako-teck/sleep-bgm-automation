@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist ..\venv (
    echo ❌ 仮想環境が見つかりません
    echo setup.bat を先に実行してください
    pause
    exit /b 1
)

echo ========================================
echo 🎨 半自動モードGUI起動
echo ========================================
echo.
echo 仮想環境のPythonを使用します...
echo.

REM 仮想環境のPythonを直接指定
..\venv\Scripts\python.exe manual_mode_v2.py

if errorlevel 1 (
    echo.
    echo ❌ エラーが発生しました
    pause
)
pause

