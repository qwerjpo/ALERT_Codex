@echo off
REM ============================================================
REM  World Monitor - Windows setup script
REM  Just double-click this file to set up.
REM ============================================================
chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "%~dp0.."

echo =====================================================
echo   World Monitor - Windows setup
echo =====================================================
echo Working directory: %CD%
echo.

REM --- Step 1: locate a real Python ----------------------------
set "PYEXE="
where py >nul 2>nul
if not errorlevel 1 (
    set "PYEXE=py -3"
    py -3 --version
) else (
    where python >nul 2>nul
    if not errorlevel 1 (
        for /f "delims=" %%p in ('where python') do (
            if not defined PYEXE (
                echo %%p | findstr /i "WindowsApps" >nul
                if errorlevel 1 (
                    set "PYEXE=%%p"
                )
            )
        )
        if not defined PYEXE (
            echo [ERROR] The "python" on PATH is the Microsoft Store stub.
            echo It cannot create virtual environments.
            echo.
            echo Please install the real Python from:
            echo    https://www.python.org/downloads/windows/
            echo.
            echo During installation tick "Add python.exe to PATH".
            echo Also disable the Store alias from:
            echo   Settings -^> Apps -^> Advanced app settings -^> App execution aliases
            echo   Turn OFF "App Installer python.exe" / "python3.exe".
            echo.
            pause
            exit /b 1
        )
    )
)

if not defined PYEXE (
    echo [ERROR] Python not found.
    echo Install Python 3.10+ from https://www.python.org/downloads/windows/
    echo and tick "Add python.exe to PATH".
    pause
    exit /b 1
)

echo Using Python: %PYEXE%
%PYEXE% --version
if errorlevel 1 (
    echo [ERROR] Python launcher returned an error.
    pause
    exit /b 1
)
echo.

REM --- Step 2: clean broken .venv ------------------------------
if exist ".venv" (
    if not exist ".venv\Scripts\python.exe" (
        echo Detected a broken .venv folder. Removing it ...
        rmdir /s /q ".venv"
    )
)

REM --- Step 3: create venv -------------------------------------
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment .venv ...
    %PYEXE% -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create venv.
        echo You may be missing the venv module. Try reinstalling Python.
        pause
        exit /b 1
    )
)

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] .venv\Scripts\python.exe was not created.
    echo The venv command appears to have silently failed.
    echo This usually means Python is the Microsoft Store stub.
    echo Please install Python from python.org instead.
    pause
    exit /b 1
)

REM --- Step 4: install dependencies ----------------------------
echo Upgrading pip ...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
    echo [WARN] pip upgrade failed; continuing anyway.
)

echo.
echo Installing dependencies ^(first run takes a few minutes^) ...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Dependency installation failed.
    echo Check your internet connection or proxy settings.
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
