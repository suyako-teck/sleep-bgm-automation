@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                      🧪 自動テスト実行 🧪                        ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo システム全体の動作確認を行います
echo 所要時間: 約30秒
echo.

if not exist ..\venv\Scripts\python.exe (
    echo ❌ 仮想環境が見つかりません
    echo setup.bat を先に実行してください
    pause
    exit /b 1
)

..\venv\Scripts\python.exe auto_test.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo ⚠️  テストが失敗しました
    echo ========================================
    echo.
    echo 対処方法:
    echo   1. エラーメッセージを確認
    echo   2. setup.bat を再実行
    echo   3. reinstall.bat を実行
    echo   4. TROUBLESHOOTING.md を参照
    echo.
) else (
    echo.
    echo ========================================
    echo ✅ システムは正常です
    echo ========================================
    echo.
    echo 次のステップ:
    echo   manual.bat を実行して動画を生成できます
    echo.
)

pause

