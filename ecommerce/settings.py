"""
This settings file imports all settings from the inner ecommerce module.
"""

import os
import sys
import logging


# Set up logging
logging.basicConfig(filename='/tmp/settings_debug.log', level=logging.DEBUG)
logging.debug("Loading bridge settings file")

# Get current directory and add it to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
logging.debug(f"Current directory: {current_dir}")

# Add parent directory to Python path if needed
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    logging.debug(f"Added parent directory to sys.path: {parent_dir}")

# Add the inner ecommerce directory to Python path
inner_dir = os.path.join(current_dir, 'ecommerce')
if inner_dir not in sys.path:
    sys.path.insert(0, inner_dir)
    logging.debug(f"Added inner ecommerce directory to sys.path: {inner_dir}")

# Import settings from the inner settings file
try:
    from ecommerce.settings import *
    logging.debug("Successfully imported settings from ecommerce.settings")
except Exception as e:
    logging.error(f"Error importing inner settings: {e}")
    import traceback
    logging.error(traceback.format_exc())
    raise

# Update ALLOWED_HOSTS to include Render domain
render_host = os.environ.get('ALLOWED_HOSTS', '')
if render_host and render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_host)
    logging.debug(f"Added {render_host} to ALLOWED_HOSTS")

# Always allow onrender.com domains
if '.onrender.com' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('.onrender.com')
    logging.debug("Added .onrender.com to ALLOWED_HOSTS")
    
# Add specific Render hostname
if 'e-commerce-django-f4um.onrender.com' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('e-commerce-django-f4um.onrender.com')
    logging.debug("Added e-commerce-django-f4um.onrender.com to ALLOWED_HOSTS")

# Print the final ALLOWED_HOSTS for debugging
logging.debug(f"Final ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# Ensure ROOT_URLCONF is properly set
ROOT_URLCONF = 'ecommerce.urls'
logging.debug(f"ROOT_URLCONF set to: {ROOT_URLCONF}") 