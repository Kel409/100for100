@echo off
rem Launch the Image Library app. First run sets up the environment.
cd /d "%~dp0"

if not exist ".venv\Scripts\pythonw.exe" (
    echo First run: setting up the environment, please wait...
    py -m venv .venv
    call ".venv\Scripts\activate.bat"
    pip install -e .
    if errorlevel 1 (
        echo Setup failed. Make sure Python 3.9+ is installed and on PATH.
        pause
        exit /b 1
    )
)

start "" "%~dp0.venv\Scripts\pythonw.exe" -m QuickBar
