import os
import sys

# Add the project root to the python path so Vercel can find 'backend'
path = os.path.dirname(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)

# Set the settings module before importing application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

from backend.wsgi import application

# This is the entry point for Vercel
app = application
