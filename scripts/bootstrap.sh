#!/usr/bin/env bash
set -euo pipefail
python --version
python -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
if [ ! -f instance/portal.sqlite ]; then
  .venv/bin/python -m flask --app app init-db
fi
printf '\nReady. Run: source .venv/bin/activate\nThen: python -m flask --app app run --host 0.0.0.0 --port 5000\n'
