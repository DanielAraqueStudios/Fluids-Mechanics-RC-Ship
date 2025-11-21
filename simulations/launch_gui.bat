@echo off
REM RC Cargo Barge Analysis Dashboard - Windows Launcher
REM Universidad Militar Nueva Granada

echo ============================================================
echo   RC CARGO BARGE - ANALYSIS DASHBOARD
echo   Universidad Militar Nueva Granada
echo ============================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from python.org
    pause
    exit /b 1
)

echo [1/3] Checking Python version...
python --version

echo.
echo [2/3] Checking dependencies...
python -c "import PyQt6; print('PyQt6: OK')" 2>nul
if errorlevel 1 (
    echo PyQt6 not found. Installing dependencies...
    pip install -r requirements_gui.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Dependencies: OK
)

echo.
echo [3/3] Launching dashboard...
echo.
python hull_analysis_gui.py

if errorlevel 1 (
    echo.
    echo ERROR: Application crashed or failed to start
    echo Check the error messages above
    pause
)
