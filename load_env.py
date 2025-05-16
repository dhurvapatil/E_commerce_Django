"""
Load environment variables for Django.
"""

import os
import logging

# Set up logging
logging.basicConfig(filename='/tmp/load_env.log', level=logging.DEBUG)
logging.debug("Loading environment variables")

# Set default environment variables for Render deployment
def setup_env():
    """Set up environment variables for Render deployment."""
    
    # Required environment variables
    env_vars = {
        'DJANGO_SETTINGS_MODULE': 'settings',
        'DEBUG': 'False',
        'ALLOWED_HOSTS': 'e-commerce-django-f4um.onrender.com,.onrender.com'
    }
    
    # Set environment variables if not already set
    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value
            logging.debug(f"Set {key}={value}")
    
    logging.debug(f"Final environment variables: DJANGO_SETTINGS_MODULE={os.environ.get('DJANGO_SETTINGS_MODULE')}, DEBUG={os.environ.get('DEBUG')}, ALLOWED_HOSTS={os.environ.get('ALLOWED_HOSTS')}")

# Execute when imported
setup_env() 