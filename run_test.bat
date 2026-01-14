@echo off
REM Test runner script for Windows
REM Activates virtual environment and runs pytest

setlocal enabledelayedexpansion

if not exist venv (
    echo Virtual environment not found. Please run setup.bat first.
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Running pytest...
pytest -v tests/

if !errorlevel! neq 0 (
    echo Tests failed with exit code !errorlevel!
    exit /b !errorlevel!
)

echo All tests passed!
