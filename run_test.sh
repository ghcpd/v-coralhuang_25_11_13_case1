#!/bin/bash
# Test runner script for Linux/macOS
# Activates virtual environment and runs pytest

set -e

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Running pytest..."
pytest -v tests/

echo "All tests passed!"
