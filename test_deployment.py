#!/usr/bin/env python
"""
Test script to verify deployment configuration.
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(filename='/tmp/test_deployment.log', level=logging.DEBUG)
logging.debug("Starting deployment test")

# Log the current directory and Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
logging.debug(f"Current directory: {current_dir}")
logging.debug(f"Python path: {sys.path}")

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
logging.debug(f"DJANGO_SETTINGS_MODULE set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

try:
    # Import Django settings
    from django.conf import settings
    logging.debug(f"Django settings imported successfully")
    logging.debug(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    logging.debug(f"DEBUG: {settings.DEBUG}")
    logging.debug(f"ROOT_URLCONF: {settings.ROOT_URLCONF}")
    logging.debug(f"WSGI_APPLICATION: {settings.WSGI_APPLICATION}")
    logging.debug(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    logging.debug(f"STATIC_URL: {settings.STATIC_URL}")
    logging.debug(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    
    # Import Django WSGI application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    logging.debug("Django WSGI application imported successfully")
    
    # Import URLs
    import urls
    logging.debug(f"URLs imported successfully: {urls.urlpatterns}")
    
    # Print success message
    print("Deployment test successful!")
    logging.debug("Deployment test successful!")
except Exception as e:
    logging.error(f"Error during deployment test: {e}")
    import traceback
    logging.error(traceback.format_exc())
    print(f"Error during deployment test: {e}")
    sys.exit(1) 