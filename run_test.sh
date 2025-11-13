#!/usr/bin/env bash
set -e
if [[ -f .venv/bin/activate ]]; then
  . .venv/bin/activate
fi
pytest -q
