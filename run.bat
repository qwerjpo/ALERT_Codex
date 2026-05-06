@echo off
REM ============================================================
REM  World Monitor - launcher (Windows)
REM  Double-click to start the server and open the dashboard.
REM ============================================================
chcp 65001 >nul
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found.
    echo.
    echo Please run scripts\setup.bat first.
    echo.
    pause
    exit /b 1
)

echo =====================================================
echo   Starting World Monitor ...
echo   Dashboard: http://127.0.0.1:8000
echo =====================================================
echo.
echo ^(Closing this window will stop the server.^)
echo.

REM Open the browser after 3 seconds
start "" /b cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:8000"

".venv\Scripts\python.exe" -m backend.main
pause
