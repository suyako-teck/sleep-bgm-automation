@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist ..\venv (
    echo ❌ 仮想環境なし
    echo setup.bat を実行してください
    pause
    exit /b 1
)

if not exist credentials.json (
    echo ❌ credentials.json がありません
    echo Google Cloud Consoleから取得してください
    pause
    exit /b 1
)

echo YouTube認証を開始します...
echo 仮想環境のPythonを使用します...
echo.

REM 仮想環境のPythonを直接指定
..\venv\Scripts\python.exe scripts\setup_youtube_auth.py

if errorlevel 1 (
    echo.
    echo ❌ 認証エラーが発生しました
)
pause

