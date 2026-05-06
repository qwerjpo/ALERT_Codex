@echo off
REM ============================================================
REM  World Monitor - 起動 (Windows)
REM  ダブルクリックでサーバを起動し、ブラウザを開きます
REM ============================================================
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] 仮想環境が見つかりません。
    echo.
    echo まず scripts\setup.bat をダブルクリックして
    echo セットアップを実行してください。
    echo.
    pause
    exit /b 1
)

echo =====================================================
echo   World Monitor を起動中...
echo   ダッシュボード: http://127.0.0.1:8000
echo =====================================================
echo.
echo ^（このウィンドウを閉じるとサーバが停止します^）
echo.

REM 3 秒後にブラウザを自動オープン
start "" /b cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:8000"

".venv\Scripts\python.exe" -m backend.main
pause
