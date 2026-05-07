@echo off
REM  World Monitor - Windows setup. Double-click to run.
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0.."
echo =====================================================
echo   World Monitor - Windows setup
echo =====================================================
echo Working directory: %CD%
echo.
set "PYEXE="
where py >nul 2>nul
if not errorlevel 1 (set "PYEXE=py -3" & py -3 --version) else (
    where python >nul 2>nul
    if not errorlevel 1 (
        for /f "delims=" %%p in ('where python') do (
            if not defined PYEXE (
                echo %%p | findstr /i "WindowsApps" >nul
                if errorlevel 1 (set "PYEXE=%%p")
            )
        )
        if not defined PYEXE (
            echo [ERROR] Python on PATH is Microsoft Store stub.
            echo Install real Python from https://www.python.org/downloads/windows/
            echo During install tick "Add python.exe to PATH".
            echo Disable Store alias: Settings-^>Apps-^>Advanced app settings-^>App execution aliases
            pause & exit /b 1
        )
    )
)
if not defined PYEXE (echo [ERROR] Python not found. & echo Install from https://www.python.org/downloads/windows/ & pause & exit /b 1)
echo Using: %PYEXE% & %PYEXE% --version
echo.
if exist ".venv" if not exist ".venv\Scripts\python.exe" (echo Removing broken .venv ... & rmdir /s /q ".venv")
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment ...
    %PYEXE% -m venv .venv
    if errorlevel 1 (echo [ERROR] venv creation failed. & pause & exit /b 1)
)
if not exist ".venv\Scripts\python.exe" (echo [ERROR] .venv\Scripts\python.exe missing. Python may be Store stub. & pause & exit /b 1)
echo Upgrading pip ...
".venv\Scripts\python.exe" -m pip install --upgrade pip
echo.
echo Installing dependencies (first run takes a few minutes) ...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (echo [ERROR] Install failed. Check internet connection. & pause & exit /b 1)
echo.
echo =====================================================
echo   Setup complete! Double-click run.bat to start.
echo =====================================================
echo.
pause
