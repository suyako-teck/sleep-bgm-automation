@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist ..\venv (
    echo ❌ 仮想環境が見つかりません
    echo setup.bat を先に実行してください
    pause
    exit /b 1
)

call ..\venv\Scripts\activate.bat

echo ========================================
echo 🎨 半自動モードGUI起動
echo ========================================
echo.
python manual_mode_v2.py
pause

