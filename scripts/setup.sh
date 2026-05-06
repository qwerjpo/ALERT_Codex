#!/usr/bin/env bash
# World Monitor — one-shot setup script for Linux / macOS.
#
# Usage:
#   ./scripts/setup.sh           # creates .venv, installs deps
#   ./scripts/setup.sh run       # also starts the server

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d ".venv" ]; then
  echo ">> creating virtualenv .venv"
  python3 -m venv .venv
fi

echo ">> installing dependencies"
.venv/bin/pip install --upgrade pip >/dev/null
.venv/bin/pip install -r requirements.txt

if [ "${1:-}" = "run" ]; then
  echo ">> starting World Monitor on http://127.0.0.1:8000"
  exec .venv/bin/python -m backend.main
else
  echo ""
  echo "Setup complete. Start the dashboard with:"
  echo ""
  echo "  source .venv/bin/activate && python -m backend.main"
  echo ""
fi
