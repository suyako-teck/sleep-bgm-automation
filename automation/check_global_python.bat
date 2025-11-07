@echo off
chcp 65001 >nul
echo ========================================
echo グローバルPython環境チェック
echo ========================================
echo.

echo [Pythonパス確認]
where python
echo.

echo [グローバルPythonバージョン]
python --version
echo.

echo [グローバルPythonの場所]
python -c "import sys; print('実行パス:', sys.executable)"
python -c "import sys; print('ベースパス:', sys.base_prefix)"
echo.

echo ========================================
echo インストール済みパッケージ（グローバル）
echo ========================================
echo.

REM 一時ファイルに出力
python -m pip list --format=columns > temp_global_packages.txt

REM パッケージ数をカウント
for /f %%A in ('python -m pip list ^| find /c /v ""') do set count=%%A
echo 合計パッケージ数: %count%
echo.

echo [大容量パッケージを検出中...]
echo.

REM 大容量の可能性があるパッケージをチェック
python -c "import sys; import subprocess; result = subprocess.run([sys.executable, '-m', 'pip', 'list'], capture_output=True, text=True); packages = result.stdout.lower(); large_packages = ['torch', 'tensorflow', 'opencv', 'scipy', 'numpy', 'pandas', 'matplotlib', 'pillow', 'moviepy', 'pydub', 'google-api', 'google-auth']; found = [pkg for pkg in large_packages if pkg in packages]; print('\n'.join(found) if found else 'なし')" > temp_large_packages.txt

echo 検出された大容量パッケージ:
type temp_large_packages.txt
echo.

REM 詳細なパッケージリスト表示
echo.
echo ========================================
echo 全パッケージリスト:
echo ========================================
type temp_global_packages.txt
echo.

echo ========================================
echo チェック完了
echo ========================================
echo.

REM パッケージ数が多い場合は警告
if %count% GTR 50 (
    echo ⚠️  警告: グローバル環境に%count%個のパッケージがインストールされています
    echo.
    echo 推奨対応:
    echo   1. このプロジェクトでは仮想環境を使用しています
    echo   2. グローバル環境はクリーンに保つことを推奨します
    echo   3. 不要なパッケージを削除するには cleanup_global_python.bat を実行してください
) else if %count% GTR 20 (
    echo ℹ️  グローバル環境に%count%個のパッケージがあります
    echo   仮想環境を使用しているため問題ありません
) else (
    echo ✅ グローバル環境はクリーンです（%count%個）
)
echo.

REM 一時ファイル削除
del temp_global_packages.txt
del temp_large_packages.txt

echo.
echo 詳細ログを保存するには:
echo   check_global_python.bat ^> global_check_log.txt
echo.
pause

