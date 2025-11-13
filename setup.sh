#!/usr/bin/env bash
set -euo pipefail

case "$(uname)" in
  Darwin) OS_NAME="macOS" ;;
  Linux) OS_NAME="Linux" ;;
  *) OS_NAME="Unknown" ;;
esac

echo "Detected OS: $OS_NAME"

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

# shellcheck source=/dev/null
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
