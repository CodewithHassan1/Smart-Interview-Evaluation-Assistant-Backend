#!/bin/bash
set -e

# Create and activate a virtualenv so pip installs do not attempt to
# modify the system Python (fixes PEP 668 "externally-managed-environment" errors).
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run collectstatic using the venv's Python
python manage.py collectstatic --noinput --clear
