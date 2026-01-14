#!/bin/bash
# Setup script for Linux/macOS
# Detects OS, creates virtual environment, and installs dependencies

set -e

# Detect OS
OS_TYPE=$(uname -s)

echo "Detected OS: $OS_TYPE"
echo "Creating virtual environment..."

if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping creation."
else
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
