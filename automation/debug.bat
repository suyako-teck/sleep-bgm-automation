@echo off
chcp 65001 >nul
echo ========================================
echo デバッグ情報収集
echo ========================================
echo.

cd /d "%~dp0"

echo [システム情報]
echo OS: %OS%
echo ユーザー: %USERNAME%
echo 現在のディレクトリ: %CD%
echo.

echo [Pythonバージョン]
python --version
echo.

echo [Python実行パス]
where python
echo.

echo [仮想環境の存在確認]
if exist ..\venv (
    echo ✅ venv フォルダ存在: %CD%\..\venv
) else (
    echo ❌ venv フォルダなし
)
echo.

echo [requirements.txt の存在確認]
if exist requirements.txt (
    echo ✅ requirements.txt 存在
    echo.
    echo [requirements.txt の内容]
    type requirements.txt
) else (
    echo ❌ requirements.txt なし
)
echo.

echo [仮想環境を有効化]
call ..\venv\Scripts\activate.bat
echo.

echo [仮想環境内のPython]
where python
python --version
echo.

echo [インストール済みパッケージ]
pip list
echo.

echo [重要なモジュールの確認]
python -c "import sys; print('Python実行パス:', sys.executable)"
python -c "import sys; print('仮想環境:', sys.prefix)"
echo.

echo [モジュールインポートテスト]
python -c "import pydub; print('✅ pydub')" 2>&1
python -c "import moviepy; print('✅ moviepy')" 2>&1
python -c "import PIL; print('✅ PIL')" 2>&1
python -c "import yaml; print('✅ yaml')" 2>&1
python -c "from google.oauth2 import credentials; print('✅ google.oauth2')" 2>&1
python -c "from googleapiclient import discovery; print('✅ googleapiclient')" 2>&1
echo.

echo [ファイル構造]
echo.
echo sleep/
dir /b /s ..\templates 2>nul | find /c ".md" > nul && echo   templates/ (存在) || echo   templates/ (なし)
dir /b ..\venv 2>nul > nul && echo   venv/ (存在) || echo   venv/ (なし)
echo   automation/
echo     - manual_mode_v2.py: 
if exist manual_mode_v2.py (echo       ✅ 存在) else (echo       ❌ なし)
echo     - requirements.txt: 
if exist requirements.txt (echo       ✅ 存在) else (echo       ❌ なし)
echo     - credentials.json: 
if exist credentials.json (echo       ✅ 存在) else (echo       ⚠️  なし)
echo     - token.json: 
if exist token.json (echo       ✅ 存在) else (echo       ⚠️  なし)
echo.

echo ========================================
echo デバッグ情報収集完了
echo ========================================
echo.
echo この情報をコピーしてサポートに送信してください
echo.
pause

