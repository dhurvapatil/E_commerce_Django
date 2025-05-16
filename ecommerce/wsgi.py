"""
WSGI config for ecommerce project.

This module creates the WSGI application for the project.
"""

import os
import sys

# Add the project directory to the Python path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

# Set the settings module to point to the inner ecommerce directory settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.ecommerce.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 