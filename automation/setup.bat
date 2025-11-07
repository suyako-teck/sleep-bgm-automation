@echo off
chcp 65001 >nul
echo ========================================
echo AI音楽BGM自動化ツール - セットアップ
echo ========================================
echo.

REM このバッチファイルのディレクトリに移動
cd /d "%~dp0"

echo 現在のディレクトリ: %CD%
echo.

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
REM 親ディレクトリ（sleep/）に移動
cd ..
echo 仮想環境作成場所: %CD%\venv
if exist venv (
    echo ✓ 既存の仮想環境を使用
) else (
    python -m venv venv
    echo ✓ 仮想環境作成完了
)
echo.

echo [3/4] 依存関係インストール中...
REM automationフォルダに戻る
cd automation
echo requirements.txtの場所: %CD%\requirements.txt
echo.

echo 仮想環境のPythonを使用します...
echo パス: %CD%\..\venv\Scripts\python.exe
echo.

REM pipアップグレード（仮想環境のPythonを直接指定）
echo pipをアップグレード中...
..\venv\Scripts\python.exe -m pip install --upgrade pip

if errorlevel 1 (
    echo ❌ pipアップグレード失敗
    pause
    exit /b 1
)

echo.
echo 依存関係をインストール中...
..\venv\Scripts\pip.exe install -r requirements.txt

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

