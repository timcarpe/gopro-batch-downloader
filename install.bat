@echo off
title GoPro Batch Downloader Installer
echo ===================================================
echo   GoPro Batch Downloader - Easy Installer
echo ===================================================
echo.
echo 1. Setting up Python virtual environment (.venv)...
python -m venv .venv
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python is not installed or not in your system PATH.
    echo Please install Python 3.10 or newer - make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b
)

echo.
echo 2. Installing required download libraries...
.venv\Scripts\pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install requirements. Please check your internet connection.
    echo.
    pause
    exit /b
)

echo.
echo ===================================================
echo   Setup Completed Successfully!
echo ===================================================
echo You can now run "run.bat" to start downloading your media.
echo.
pause
