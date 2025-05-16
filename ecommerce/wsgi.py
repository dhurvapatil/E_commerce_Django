"""
WSGI config for ecommerce project.

This module creates the WSGI application for the project.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    # Log any errors for debugging
    import traceback
    with open('/tmp/wsgi_error.log', 'w') as f:
        f.write(f"Error loading application: {str(e)}\n")
        f.write(traceback.format_exc())
    raise 