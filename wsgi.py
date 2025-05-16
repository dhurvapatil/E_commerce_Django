"""
WSGI config for ecommerce project at the root level.
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(filename='/tmp/wsgi_root_debug.log', level=logging.DEBUG)
logging.debug("Starting WSGI application loading from root wsgi.py")

# Get current directory and add it to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
logging.debug(f"Current directory: {current_dir}")

# Add the inner ecommerce directory to Python path if needed
ecommerce_dir = os.path.join(current_dir, 'ecommerce')
if ecommerce_dir not in sys.path:
    sys.path.insert(0, ecommerce_dir)
    logging.debug(f"Added ecommerce directory to sys.path: {ecommerce_dir}")

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
logging.debug(f"DJANGO_SETTINGS_MODULE set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

# Log Python path
logging.debug(f"Python path: {sys.path}")
logging.debug(f"Current directory contents: {os.listdir(current_dir)}")

# Explicitly set ALLOWED_HOSTS in environment variables
if 'ALLOWED_HOSTS' not in os.environ:
    os.environ['ALLOWED_HOSTS'] = 'e-commerce-django-f4um.onrender.com,.onrender.com'
    logging.debug("Set ALLOWED_HOSTS environment variable")

# Try to directly modify ALLOWED_HOSTS
try:
    from django.conf import settings
    if 'e-commerce-django-f4um.onrender.com' not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS.append('e-commerce-django-f4um.onrender.com')
    if '.onrender.com' not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS.append('.onrender.com')
    logging.debug(f"Updated ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
except Exception as e:
    logging.error(f"Error updating ALLOWED_HOSTS: {e}")

# Apply deployment overrides
try:
    import deployment_overrides
    deployment_overrides.override_settings()
    logging.debug("Applied deployment overrides")
except Exception as e:
    logging.error(f"Error applying deployment overrides: {e}")

try:
    # Import the Django WSGI application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    logging.debug("Successfully loaded WSGI application")
except Exception as e:
    logging.error(f"Error loading application: {str(e)}")
    import traceback
    logging.error(traceback.format_exc())
    raise 