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

echo 仮想環境を有効化中...
call ..\venv\Scripts\activate.bat

echo.
echo pipをアップグレード中...
python -m pip install --upgrade pip

echo.
echo 既存のパッケージをアンインストール中...
pip freeze > temp_requirements.txt
pip uninstall -y -r temp_requirements.txt
del temp_requirements.txt

echo.
echo パッケージを再インストール中...
pip install -r requirements.txt

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
pip list
echo.
pause

