@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist ..\venv (
    echo ❌ 仮想環境なし
    echo setup.bat を実行してください
    pause
    exit /b 1
)

call ..\venv\Scripts\activate.bat

if not exist credentials.json (
    echo ❌ credentials.json がありません
    echo Google Cloud Consoleから取得してください
    pause
    exit /b 1
)

python setup_youtube_auth.py
pause

