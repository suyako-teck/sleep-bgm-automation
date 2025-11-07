@echo off
chcp 65001 >nul
echo ========================================
echo Python環境比較
echo ========================================
echo.

echo [グローバルPython環境]
echo ----------------------------------------
python --version
python -c "import sys; print('パス:', sys.executable)"
echo.
echo パッケージ数:
for /f %%A in ('python -m pip list ^| find /c /v ""') do echo   %%A 個
echo.

echo [仮想環境]
echo ----------------------------------------
if exist ..\venv\Scripts\python.exe (
    ..\venv\Scripts\python.exe --version
    ..\venv\Scripts\python.exe -c "import sys; print('パス:', sys.executable)"
    echo.
    echo パッケージ数:
    for /f %%A in ('..\venv\Scripts\pip.exe list ^| find /c /v ""') do echo   %%A 個
) else (
    echo ❌ 仮想環境が見つかりません
    echo setup.bat を実行してください
)
echo.

echo ========================================
echo パッケージ比較
echo ========================================
echo.

echo [グローバル環境のみにあるパッケージ]
python -m pip list > temp_global.txt
..\venv\Scripts\pip.exe list > temp_venv.txt

python -c "global_pkgs = set(line.split()[0].lower() for line in open('temp_global.txt').readlines()[2:] if line.strip()); venv_pkgs = set(line.split()[0].lower() for line in open('temp_venv.txt').readlines()[2:] if line.strip()); global_only = global_pkgs - venv_pkgs; [print(f'  - {pkg}') for pkg in sorted(global_only)] if global_only else print('  なし')"
echo.

echo [仮想環境のみにあるパッケージ]
python -c "global_pkgs = set(line.split()[0].lower() for line in open('temp_global.txt').readlines()[2:] if line.strip()); venv_pkgs = set(line.split()[0].lower() for line in open('temp_venv.txt').readlines()[2:] if line.strip()); venv_only = venv_pkgs - global_pkgs; [print(f'  - {pkg}') for pkg in sorted(venv_only)] if venv_only else print('  なし')"
echo.

echo [両方にあるパッケージ]
python -c "global_pkgs = set(line.split()[0].lower() for line in open('temp_global.txt').readlines()[2:] if line.strip()); venv_pkgs = set(line.split()[0].lower() for line in open('temp_venv.txt').readlines()[2:] if line.strip()); both = global_pkgs.intersection(venv_pkgs); [print(f'  - {pkg}') for pkg in sorted(both)] if both else print('  なし')"
echo.

del temp_global.txt
del temp_venv.txt

echo ========================================
echo 推奨事項
echo ========================================
echo.

echo ✅ このプロジェクトは仮想環境を使用しています
echo ✅ manual.bat から起動すれば仮想環境が使われます
echo.
echo グローバル環境に不要なパッケージがある場合:
echo   cleanup_global_python.bat を実行してください
echo.
pause

