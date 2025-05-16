"""
WSGI config for ecommerce project.
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(filename='/tmp/wsgi_debug.log', level=logging.DEBUG)
logging.debug("Starting WSGI application loading")

# Get current directory and add it to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
logging.debug(f"Current directory: {current_dir}")
logging.debug(f"Path: {sys.path}")
logging.debug(f"Directory contents: {os.listdir(current_dir)}")

# Set the settings module to use the directly accessible settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
logging.debug(f"DJANGO_SETTINGS_MODULE set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    logging.debug("Successfully loaded WSGI application")
except Exception as e:
    logging.error(f"Error loading application: {str(e)}")
    import traceback
    logging.error(traceback.format_exc())
    raise 