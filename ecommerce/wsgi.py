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

# Add parent directory to sys.path if needed
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    logging.debug(f"Added parent directory to sys.path: {parent_dir}")

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
logging.debug(f"DJANGO_SETTINGS_MODULE set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

# Debug information
logging.debug(f"Python path: {sys.path}")
logging.debug(f"Directory contents: {os.listdir(current_dir)}")

try:
    # Make sure we can access the inner ecommerce module
    inner_ecommerce_dir = os.path.join(current_dir, 'ecommerce')
    if os.path.exists(inner_ecommerce_dir) and inner_ecommerce_dir not in sys.path:
        sys.path.insert(0, inner_ecommerce_dir)
        logging.debug(f"Added inner ecommerce directory to sys.path: {inner_ecommerce_dir}")
    
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    logging.debug("Successfully loaded WSGI application")
except Exception as e:
    logging.error(f"Error loading application: {str(e)}")
    import traceback
    logging.error(traceback.format_exc())
    raise 