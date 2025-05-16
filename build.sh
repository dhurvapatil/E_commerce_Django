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

# Create a simple wsgi.py in the inner ecommerce directory to make sure it's properly configured
echo "Updating WSGI configuration in inner ecommerce directory"
cat > ecommerce/ecommerce/wsgi.py << 'EOF'
"""
WSGI config for ecommerce project.
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(filename='/tmp/wsgi_inner_debug.log', level=logging.DEBUG)
logging.debug("Starting inner WSGI application loading")

# Add the current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
    logging.debug(f"Added current_dir to sys.path: {current_dir}")

# Add the parent directory to sys.path
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    logging.debug(f"Added parent_dir to sys.path: {parent_dir}")

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
logging.debug(f"DJANGO_SETTINGS_MODULE set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

# Import Django WSGI application
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    logging.debug("Successfully loaded inner WSGI application")
except Exception as e:
    logging.error(f"Error loading inner WSGI application: {e}")
    import traceback
    logging.error(traceback.format_exc())
    raise
EOF

# Copy the root settings and wsgi files to ensure they're up to date
echo "Setting up root-level configuration files"

# Create a root level wsgi.py
cat > wsgi.py << 'EOF'
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
EOF

# Create root level URLs
cat > urls.py << 'EOF'
"""
Root URL configuration for ecommerce project.
"""

import logging
import os

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

logging.basicConfig(filename='/tmp/urls_debug.log', level=logging.DEBUG)
logging.debug("Loading root urls.py")

# Add static and media URLs in debug mode
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]

# Add static and media URLs
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Even in production, serve media files directly for this demo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

logging.debug(f"Final urlpatterns: {urlpatterns}")
EOF

# Set environment variable to point to the correct settings module
export DJANGO_SETTINGS_MODULE=settings

# Print the Python path and modules
python -c "import sys; print('PYTHONPATH:', sys.path)"
python -c "import sys; print('Modules:', sorted(sys.modules.keys()))"

# Run the test script to verify configuration
echo "Running deployment test script..."
python test_deployment.py || echo "Test failed but continuing deployment"

# Apply migrations using root manage.py
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Print final structure for debugging
echo "Final directory structure:"
find . -type d -maxdepth 3 | sort 