@echo off
chcp 65001 >nul
echo ========================================
echo プロジェクトクリーンアップ
echo ========================================
echo.

cd /d "%~dp0"

echo 不要なファイルを削除します...
echo.

REM 一時ファイル
del /q "ダウンローダー-*.code-workspace" 2>nul

REM 古いバッチファイル（使用済み）
del /q "automation\reorganize_automation.bat" 2>nul

REM 出力ファイル（ユーザーが必要に応じて削除）
echo [出力ファイル]
if exist "automation\output\*.mp4" (
    echo   ⚠️  automation\output\ に動画ファイルがあります
    set /p delete_output="   削除しますか？ (y/n): "
    if /i "%delete_output%"=="y" (
        del /q "automation\output\*.mp4" 2>nul
        del /q "automation\output\*.mp3" 2>nul
        echo   ✓ 削除しました
    )
) else (
    echo   ✓ 出力ファイルなし
)
echo.

REM キャッシュファイル
echo [キャッシュファイル削除]
if exist "automation\__pycache__" (
    rmdir /s /q "automation\__pycache__"
    echo   ✓ automation\__pycache__
)
if exist "automation\modules\__pycache__" (
    rmdir /s /q "automation\modules\__pycache__"
    echo   ✓ automation\modules\__pycache__
)
echo.

REM 背景画像（自動生成されるため削除OK）
if exist "automation\backgrounds\default_bg.png" (
    del /q "automation\backgrounds\default_bg.png" 2>nul
    echo   ✓ デフォルト背景（再生成されます）
)
echo.

echo ========================================
echo クリーンアップ完了
echo ========================================
echo.
echo クリーンな状態になりました！
echo.
pause

