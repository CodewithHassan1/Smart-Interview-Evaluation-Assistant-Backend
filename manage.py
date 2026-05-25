#!/usr/bin/env python
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:
    # If python-dotenv is not available in the build environment,
    # provide a no-op `load_dotenv` so builds that run management
    # commands before dependencies are installed don't crash.
    def load_dotenv(path=None):
        return None

def main():
    load_dotenv(Path(__file__).resolve().parent / ".env")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
