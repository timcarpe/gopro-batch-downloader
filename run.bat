@echo off
title GoPro Batch Downloader
echo ===================================================
echo   GoPro Batch Downloader
echo ===================================================
echo.
if not exist .venv (
    echo [WARNING] Virtual environment not found. Running installer first...
    call install.bat
)

set LIMIT=%1

if "%LIMIT%"=="" (
    echo How many files would you like to download?
    echo.
    echo   - Press ENTER to download everything
    echo   - Or type a number (e.g. 10) to download only that many
    echo.
    set /p LIMIT="Your choice: "
)

if "%LIMIT%"=="" (
    echo.
    echo Downloading ALL files...
    .venv\Scripts\python main.py
) else if "%LIMIT%"=="all" (
    echo.
    echo Downloading ALL files...
    .venv\Scripts\python main.py
) else (
    echo.
    echo Downloading up to %LIMIT% files...
    .venv\Scripts\python main.py --limit %LIMIT%
)

echo.
echo Process complete.
pause
