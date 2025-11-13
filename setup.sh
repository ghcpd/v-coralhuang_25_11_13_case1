#!/usr/bin/env bash

# Setup script (Linux/macOS). Creates venv and installs deps.
set -e
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. Activate the venv with: source .venv/bin/activate"
