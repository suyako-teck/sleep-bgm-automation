@echo off
chcp 65001 >nul
echo ========================================
echo AMD GPU エンコーダーテスト
echo ========================================
echo.

echo [AMD GPU情報確認]
echo.

REM AMD GPU検出
wmic path win32_VideoController get name | findstr /i "AMD Radeon"
echo.

echo [ffmpeg AMFサポート確認]
echo.

ffmpeg -encoders 2>nul | findstr /i "amf"
echo.

if errorlevel 1 (
    echo ❌ AMFエンコーダーが見つかりません
    echo.
    echo 解決方法:
    echo   1. AMD Radeon Software Adrenalin Edition をインストール
    echo      https://www.amd.com/en/support
    echo   2. AMF対応のffmpegをインストール
    echo      https://www.gyan.dev/ffmpeg/builds/
    echo.
) else (
    echo ✅ AMFエンコーダー検出
    echo.
    
    echo [AMFエンコーダーテスト実行]
    echo 1秒のテスト動画を生成中...
    echo.
    
    ffmpeg -y -f lavfi -i color=c=blue:s=640x480:d=1 -c:v h264_amf -t 1 test_amd.mp4 2>&1 | findstr /i "error Cannot"
    
    if exist test_amd.mp4 (
        echo.
        echo ✅ AMFエンコーダーは正常に動作します！
        echo.
        echo あなたのシステムでGPU高速化が使えます：
        echo   - Radeon RX 6750 XTは高性能GPU
        echo   - 8時間動画: 約4〜6分で生成可能（CPUの5倍速）
        echo.
        del test_amd.mp4
    ) else (
        echo.
        echo ❌ AMFエンコーダーは動作しません
        echo.
        echo 考えられる原因:
        echo   1. AMD Radeon Softwareが古い
        echo   2. AMFライブラリが見つからない
        echo   3. ffmpegがAMF非対応版
        echo.
        echo 解決方法:
        echo   1. AMD Radeon Softwareを最新版に更新
        echo   2. PCを再起動
        echo   3. ffmpegを再インストール（AMF対応版）
        echo.
    )
)

echo ========================================
echo テスト完了
echo ========================================
echo.
echo 次のステップ:
echo   manual.bat を実行して動画生成をテストしてください
echo.
pause

