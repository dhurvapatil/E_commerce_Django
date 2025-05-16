"""
WSGI config for ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(filename='/tmp/wsgi_inner_debug.log', level=logging.DEBUG)
logging.debug("Starting inner WSGI application loading")

# Explicitly set ALLOWED_HOSTS in environment variables
if 'ALLOWED_HOSTS' not in os.environ:
    os.environ['ALLOWED_HOSTS'] = 'e-commerce-django-f4um.onrender.com,.onrender.com'
    logging.debug("Set ALLOWED_HOSTS environment variable")

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.ecommerce.settings')
logging.debug(f"DJANGO_SETTINGS_MODULE set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

# Add the current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_dir = os.path.dirname(parent_dir)

# Print out path information for debugging
logging.debug(f"Current directory: {current_dir}")
logging.debug(f"Parent directory: {parent_dir}")
logging.debug(f"Project directory: {project_dir}")

# Add the project directory to sys.path
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)
    logging.debug(f"Added project directory to sys.path: {project_dir}")

# Add the parent directory to sys.path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    logging.debug(f"Added parent directory to sys.path: {parent_dir}")

# Try to directly modify ALLOWED_HOSTS for the settings
try:
    from django.conf import settings
    if 'e-commerce-django-f4um.onrender.com' not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS.append('e-commerce-django-f4um.onrender.com')
    if '.onrender.com' not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS.append('.onrender.com')
    logging.debug(f"Updated ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
except Exception as e:
    logging.error(f"Error updating ALLOWED_HOSTS: {e}")

try:
    # Import the Django WSGI application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    logging.debug("Successfully loaded WSGI application")
    
    # Log urls information for debugging
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        logging.debug(f"URL patterns: {len(resolver.url_patterns)} patterns found")
        logging.debug(f"Root URLconf: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    except Exception as e:
        logging.error(f"Error inspecting URLs: {e}")
        
except Exception as e:
    logging.error(f"Error loading application: {str(e)}")
    import traceback
    logging.error(traceback.format_exc())
    raise
