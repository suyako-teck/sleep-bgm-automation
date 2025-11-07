@echo off
chcp 65001 >nul
echo ========================================
echo 依存関係を再インストール
echo ========================================
echo.

cd /d "%~dp0"

if not exist ..\venv (
    echo ❌ 仮想環境が見つかりません
    echo setup.bat を先に実行してください
    pause
    exit /b 1
)

echo 仮想環境のPythonを使用します...
echo パス: %CD%\..\venv\Scripts\python.exe
echo.

echo pipをアップグレード中...
..\venv\Scripts\python.exe -m pip install --upgrade pip

if errorlevel 1 (
    echo ❌ pipアップグレード失敗
    pause
    exit /b 1
)

echo.
echo 既存のパッケージをアンインストール中...
..\venv\Scripts\pip.exe freeze > temp_requirements.txt
..\venv\Scripts\pip.exe uninstall -y -r temp_requirements.txt
del temp_requirements.txt

echo.
echo パッケージを再インストール中...
..\venv\Scripts\pip.exe install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ インストール失敗
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 再インストール完了！
echo ========================================
echo.
echo インストールされたパッケージ:
..\venv\Scripts\pip.exe list
echo.
pause

