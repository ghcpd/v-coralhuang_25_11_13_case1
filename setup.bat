@echo off
REM Setup script for Windows
REM Creates a virtual environment and installs dependencies

setlocal enabledelayedexpansion

echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping creation.
) else (
    python -m venv venv
    if !errorlevel! neq 0 (
        echo Error creating virtual environment
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo Error installing dependencies
    exit /b 1
)

echo Setup complete!
echo To activate the virtual environment, run: venv\Scripts\activate.bat
