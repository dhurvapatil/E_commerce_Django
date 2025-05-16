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
    cp -f ecommerce/ecommerce/settings.py ecommerce/settings.py.orig
    cat > ecommerce/settings.py << 'EOF'
"""
This settings file acts as a bridge to the actual settings module.
"""

import os
import sys

# Get current directory and add it to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import all settings from the inner settings module
from ecommerce.settings import *
EOF
fi

# Set environment variable to point to the correct settings module
export DJANGO_SETTINGS_MODULE=settings

# Go to the ecommerce directory for all Django operations
cd ecommerce

# Print the Python path and modules
python -c "import sys; print('PYTHONPATH:', sys.path)"
python -c "import sys; print('Modules:', sorted(sys.modules.keys()))"

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Print final structure for debugging
echo "Final directory structure:"
find .. -type d -maxdepth 3 | sort 