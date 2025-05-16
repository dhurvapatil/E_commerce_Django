#!/usr/bin/env bash
# exit on error
set -o errexit

# Print the directory structure for debugging
echo "Directory structure before setup:"
find . -type d -maxdepth 3 | sort

# Make sure the static directory exists at the root level
mkdir -p static

# Make sure the static directory exists inside ecommerce directory as well
mkdir -p ecommerce/static

# Install dependencies
pip install django pillow gunicorn

# Make sure settings.py is properly set up in the ecommerce directory
if [ -f ecommerce/settings.py ]; then
    echo "settings.py already exists in ecommerce directory"
else
    echo "Creating settings.py in ecommerce directory"
    cat > ecommerce/settings.py << 'EOF'
"""
This settings file imports all settings from the inner ecommerce module.
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(filename='/tmp/settings_debug.log', level=logging.DEBUG)
logging.debug("Loading bridge settings file")

# Add this directory to the Python path
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

# Ensure ROOT_URLCONF is properly set
ROOT_URLCONF = 'ecommerce.urls'
logging.debug(f"ROOT_URLCONF set to: {ROOT_URLCONF}")
EOF
fi

# Set environment variable to point to the correct settings module
export DJANGO_SETTINGS_MODULE=ecommerce.settings

# Go to the root directory for all Django operations
cd .

# Print the Python path and modules
python -c "import sys; print('PYTHONPATH:', sys.path)"
python -c "import sys; print('Modules:', sorted(sys.modules.keys()))"

# Apply migrations
python ecommerce/manage.py migrate

# Collect static files
python ecommerce/manage.py collectstatic --noinput

# Print final structure for debugging
echo "Final directory structure:"
find . -type d -maxdepth 3 | sort 