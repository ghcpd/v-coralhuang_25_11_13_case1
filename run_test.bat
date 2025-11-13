@echo off
if not exist ".venv\Scripts\activate" (
  echo Virtual environment missing; run setup.sh manually before running this script.
  exit /b 1
)
call .venv\Scripts\activate
python -m pytest
