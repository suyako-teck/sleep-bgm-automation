@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                  🔥 システムベンチマーク 🔥                      ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo PCの性能を測定して、動画生成の推定時間を表示します
echo.

if not exist ..\venv\Scripts\python.exe (
    echo ❌ 仮想環境が見つかりません
    echo setup.bat を先に実行してください
    pause
    exit /b 1
)

..\venv\Scripts\python.exe benchmark.py

echo.
echo ========================================
echo 結果の見方
echo ========================================
echo.
echo ⭐⭐⭐⭐⭐ = 非常に高速（推奨スペック以上）
echo ⭐⭐⭐⭐   = 高速（推奨スペック）
echo ⭐⭐⭐     = 標準（最低スペック）
echo ⭐⭐       = 低速（アップグレード推奨）
echo.
echo GPUがあれば5〜10倍高速化します！
echo.
pause

