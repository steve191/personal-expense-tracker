@echo off
echo ================================================
echo Personal Expense Tracker - Build Script
echo ================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Installing required packages...
echo ------------------------------------------------
pip install ttkbootstrap python-dateutil pandas ofxtools pillow pyinstaller

if errorlevel 1 (
    echo [ERROR] Failed to install packages.
    pause
    exit /b 1
)

echo.
echo Building executable...
echo ------------------------------------------------
pyinstaller --clean --noconsole --onefile --collect-data ttkbootstrap --name "ExpenseTracker" --icon Dollar.ico main.py

if errorlevel 1 (
    echo [ERROR] Build failed.
    pause
    exit /b 1
)

echo.
echo ================================================
echo Build complete!
echo ================================================
echo.
echo Your executable is at: dist\ExpenseTracker.exe
echo.
echo You can now distribute this file to users.
echo They just need to double-click it to run.
echo ================================================
pause
