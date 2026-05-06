@echo off
REM ============================================================
REM  World Monitor - Windows setup script
REM  Just double-click this file to set up.
REM ============================================================
chcp 65001 >nul
setlocal

cd /d "%~dp0\.."

echo =====================================================
echo   World Monitor - Windows setup
echo =====================================================
echo.

REM Check Python availability
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found.
    echo.
    echo Please install Python 3.10 or newer first:
    echo   https://www.python.org/downloads/windows/
    echo.
    echo IMPORTANT: tick "Add python.exe to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Create venv if missing
if not exist ".venv" (
    echo Creating virtual environment .venv ...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create venv.
        pause
        exit /b 1
    )
)

echo Installing dependencies ^(first run takes a few minutes^) ...
".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Dependency installation failed.
    pause
    exit /b 1
)

echo.
echo =====================================================
echo   Setup complete!
echo =====================================================
echo.
echo To start the dashboard, double-click run.bat
echo.
pause
