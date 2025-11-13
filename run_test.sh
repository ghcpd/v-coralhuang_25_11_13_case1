#!/usr/bin/env bash
set -euo pipefail

if [ -f .venv/bin/activate ]; then
    . .venv/bin/activate
fi

pytest -q
