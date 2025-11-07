@echo off
chcp 65001 >nul
echo ========================================
echo AI音楽BGM自動化ツール - セットアップ
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Pythonバージョン確認...
python --version
if errorlevel 1 (
    echo ❌ Pythonがインストールされていません
    pause
    exit /b 1
)
echo ✓ Python検出
echo.

echo [2/4] 仮想環境作成中...
cd ..
if exist venv (
    echo ✓ 既存の仮想環境を使用
) else (
    python -m venv venv
    echo ✓ 仮想環境作成完了
)
cd 02_自動化ツール
echo.

echo [3/4] 依存関係インストール中...
call ..\venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ インストール失敗
    pause
    exit /b 1
)
echo ✓ 依存関係インストール完了
echo.

echo [4/4] 環境設定...
if not exist env.example (
    echo MUBERT_API_KEY=your_api_key_here > env.example
)
if not exist .env (
    copy env.example .env
    echo ✓ .env ファイル作成
    notepad .env
) else (
    echo ✓ .env ファイル存在
)
echo.

echo ========================================
echo ✅ セットアップ完了！
echo ========================================
echo.
echo 次のステップ：
echo 1. .env にMubert APIキーを設定
echo 2. Google Cloud で credentials.json を取得
echo 3. auth.bat を実行
echo 4. manual.bat を実行
echo.
pause

