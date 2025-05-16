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

# Add this directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Add the inner ecommerce directory to Python path
inner_dir = os.path.join(current_dir, 'ecommerce')
if inner_dir not in sys.path:
    sys.path.insert(0, inner_dir)

# Import * from the inner settings file
try:
    with open(os.path.join(inner_dir, 'settings.py')) as f:
        exec(f.read())
except Exception as e:
    print(f"Error loading inner settings: {e}")
    raise

# Ensure critical settings are defined
if 'ROOT_URLCONF' not in locals():
    ROOT_URLCONF = 'ecommerce.urls'
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