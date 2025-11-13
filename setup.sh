#!/usr/bin/env bash
set -euo pipefail

# Create a virtualenv and install dependencies
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Virtual environment created at $(pwd)/.venv. Run: source .venv/bin/activate" 
