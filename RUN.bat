@echo off
setlocal
cd /d "%~dp0"
title ImageToClipboardOCR Setup

echo ==========================================
echo       ImageToClipboardOCR
echo ==========================================
echo.

where py >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=py -3"
    set "PYTHONW_CMD=pyw -3"
    goto CHECK_PYTHON
)

where python >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=python"
    set "PYTHONW_CMD=pythonw"
    goto CHECK_PYTHON
)

echo Python 3 was not found.
echo Install Python 3.11 or newer from https://www.python.org/downloads/
echo During setup, enable "Add Python to PATH", then run this file again.
pause
exit /b 1

:CHECK_PYTHON
%PYTHON_CMD% --version
if errorlevel 1 (
    echo Could not start Python. Please install Python 3.11 or newer.
    pause
    exit /b 1
)

echo.
echo Checking pip...
%PYTHON_CMD% -m pip --version
if errorlevel 1 (
    %PYTHON_CMD% -m ensurepip --upgrade
    if errorlevel 1 (
        echo Could not prepare pip.
        pause
        exit /b 1
    )
)

echo.
echo Installing or updating requirements...
%PYTHON_CMD% -m pip install --upgrade -r requirements.txt
if errorlevel 1 (
    echo.
    echo Dependency installation failed. Check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Launching ImageToClipboardOCR...
start "" %PYTHONW_CMD% "%~dp0image_to_clipboard_ocr.py"
if errorlevel 1 (
    echo Could not launch the app. Try running this file again.
    pause
    exit /b 1
)
exit /b 0
