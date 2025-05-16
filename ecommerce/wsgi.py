"""
WSGI config for ecommerce project.
"""

import os
import sys
import logging

# Create a debug log file
logging.basicConfig(filename='/tmp/wsgi_debug.log', level=logging.DEBUG)
logging.debug("Starting WSGI application loading")

# Get paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add both to Python path
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

logging.debug(f"Current directory: {current_dir}")
logging.debug(f"Parent directory: {parent_dir}")
logging.debug(f"sys.path: {sys.path}")
logging.debug(f"Contents of current dir: {os.listdir(current_dir)}")

# Try to inspect for ecommerce directory
if os.path.exists(os.path.join(current_dir, 'ecommerce')):
    ecommerce_dir = os.path.join(current_dir, 'ecommerce')
    logging.debug(f"Found ecommerce dir: {ecommerce_dir}")
    logging.debug(f"Contents: {os.listdir(ecommerce_dir)}")
    
    # If settings.py exists in the inner directory, use it
    if os.path.exists(os.path.join(ecommerce_dir, 'settings.py')):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce.settings'
        logging.debug("Using ecommerce.settings as settings module")
    else:
        logging.debug("No settings.py found in inner ecommerce directory")
else:
    logging.debug("No inner ecommerce directory found")
    
# Look for settings.py at current level
if os.path.exists(os.path.join(current_dir, 'settings.py')):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    logging.debug("Using settings as settings module")

# Fallback
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce.settings'
    logging.debug("Using ecommerce.settings as fallback")

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