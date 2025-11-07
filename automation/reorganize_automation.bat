@echo off
chcp 65001 >nul
echo ========================================
echo automationフォルダを整理
echo ========================================
echo.

cd /d "%~dp0"

echo [フォルダ作成]
mkdir "scripts" 2>nul
mkdir "docs" 2>nul
mkdir "tests" 2>nul
mkdir "output" 2>nul
mkdir "backgrounds" 2>nul

echo.
echo [スクリプトファイルを整理]

REM セットアップ・実行系（トップに残す）
echo ✓ 実行ファイルはトップレベルに配置

REM Pythonスクリプトをscriptsへ
if exist "auto_test.py" move "auto_test.py" "tests\" 2>nul
if exist "benchmark.py" move "benchmark.py" "tests\" 2>nul
if exist "setup_youtube_auth.py" move "setup_youtube_auth.py" "scripts\" 2>nul

REM ドキュメントをdocsへ
if exist "QUICKSTART.md" move "QUICKSTART.md" "docs\" 2>nul
if exist "TROUBLESHOOTING.md" move "TROUBLESHOOTING.md" "docs\" 2>nul
if exist "PERFORMANCE.md" move "PERFORMANCE.md" "docs\" 2>nul
if exist "ENVIRONMENT_MANAGEMENT.md" move "ENVIRONMENT_MANAGEMENT.md" "docs\" 2>nul
if exist "AMD_GPU_SETUP.md" move "AMD_GPU_SETUP.md" "docs\" 2>nul
if exist "使い方.txt" move "使い方.txt" "docs\" 2>nul

REM テスト・診断系
if exist "test_amd_gpu.bat" move "test_amd_gpu.bat" "tests\" 2>nul
if exist "debug.bat" move "debug.bat" "tests\" 2>nul
if exist "check_global_python.bat" move "check_global_python.bat" "tests\" 2>nul
if exist "compare_environments.bat" move "compare_environments.bat" "tests\" 2>nul

echo.
echo ========================================
echo 整理完了
echo ========================================
echo.
echo 新しい構成:
echo.
echo automation/
echo   【実行ファイル】トップレベル
echo   ├─ manual.bat          ⭐ これを使う（動画作成）
echo   ├─ setup.bat           🔧 初回セットアップ
echo   ├─ auth.bat            🔐 YouTube認証
echo   ├─ test.bat            🧪 総合テスト
echo   ├─ benchmark.bat       📊 性能測定
echo   ├─ reinstall.bat       🔄 再インストール
echo   └─ cleanup_global_python.bat  🧹 環境クリーンアップ
echo.
echo   【プログラム本体】
echo   ├─ manual_mode_v2.py   🐍 GUIアプリ
echo   ├─ template_manager.py 🐍 テンプレート管理
echo   └─ modules/            📦 処理モジュール
echo.
echo   【補助ファイル】
echo   ├─ scripts/            🔧 補助スクリプト
echo   ├─ docs/              📖 ドキュメント
echo   ├─ tests/             🧪 テスト・診断
echo   ├─ output/            📁 出力先
echo   └─ backgrounds/       🖼️ 背景画像
echo.
echo   【設定ファイル】
echo   ├─ requirements.txt   📋 依存関係
echo   ├─ README.md          📖 説明
echo   ├─ credentials.json   🔑 YouTube API
echo   └─ token.json         🔐 認証トークン
echo.
pause

