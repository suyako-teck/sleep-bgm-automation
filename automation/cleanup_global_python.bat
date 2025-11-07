@echo off
chcp 65001 >nul
echo ========================================
echo グローバルPython環境クリーンアップ
echo ========================================
echo.

echo ⚠️  警告: この操作はグローバルPython環境のパッケージを削除します
echo ⚠️  このプロジェクト以外で使用しているパッケージも削除される可能性があります
echo.

echo 続行する前に確認してください:
echo   - 他のPythonプロジェクトに影響がないか
echo   - 必要なパッケージがないか
echo.

set /p confirm="本当に続行しますか? (yes と入力): "

if not "%confirm%"=="yes" (
    echo キャンセルしました
    pause
    exit /b 0
)

echo.
echo ========================================
echo クリーンアップ開始
echo ========================================
echo.

echo [現在のパッケージリスト]
python -m pip list
echo.

echo [オプション選択]
echo 1. このプロジェクト関連のパッケージのみ削除（安全）
echo 2. pip以外のすべてのパッケージを削除（危険）
echo 3. キャンセル
echo.

set /p option="選択 (1/2/3): "

if "%option%"=="3" (
    echo キャンセルしました
    pause
    exit /b 0
)

if "%option%"=="1" (
    echo.
    echo [このプロジェクト関連パッケージを削除中...]
    echo.
    
    REM プロジェクト関連の大容量パッケージ
    python -m pip uninstall -y moviepy pydub Pillow google-api-python-client google-auth-oauthlib google-auth-httplib2 pyyaml imageio imageio-ffmpeg numpy 2>nul
    
    echo ✅ クリーンアップ完了
)

if "%option%"=="2" (
    echo.
    echo [すべてのパッケージを削除中...]
    echo.
    
    python -m pip freeze > temp_all_packages.txt
    python -m pip uninstall -y -r temp_all_packages.txt
    del temp_all_packages.txt
    
    echo ✅ すべてのパッケージを削除しました
)

echo.
echo [クリーンアップ後のパッケージリスト]
python -m pip list
echo.

echo ========================================
echo クリーンアップ完了
echo ========================================
echo.

echo 次のステップ:
echo   1. このプロジェクトは仮想環境を使用します
echo   2. manual.bat から起動すれば問題ありません
echo   3. グローバル環境はクリーンに保たれます
echo.
pause

