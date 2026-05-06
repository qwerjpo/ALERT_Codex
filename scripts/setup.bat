@echo off
REM ============================================================
REM  World Monitor - Windows setup script
REM  使い方: このファイルをダブルクリックするだけ
REM ============================================================
setlocal

cd /d "%~dp0\.."

echo =====================================================
echo   World Monitor - Windows setup
echo =====================================================
echo.

REM Python の存在チェック
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python が見つかりません。
    echo.
    echo Python 3.10 以上を先にインストールしてください:
    echo   https://www.python.org/downloads/windows/
    echo.
    echo インストール時に "Add python.exe to PATH" に必ずチェックを入れてください。
    echo.
    pause
    exit /b 1
)

REM venv 作成
if not exist ".venv" (
    echo ^>^> 仮想環境 .venv を作成中...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] venv の作成に失敗しました。
        pause
        exit /b 1
    )
)

echo ^>^> 依存ライブラリをインストール中... ^(初回は数分かかります^)
".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] 依存ライブラリのインストールに失敗しました。
    pause
    exit /b 1
)

echo.
echo =====================================================
echo   セットアップ完了！
echo =====================================================
echo.
echo 起動するには run.bat をダブルクリックしてください。
echo.
pause
