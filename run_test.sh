#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  echo "Virtual environment missing; run ./setup.sh first."
  exit 1
fi

# shellcheck source=/dev/null
source .venv/bin/activate
pytest
