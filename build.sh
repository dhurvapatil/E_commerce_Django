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

# Create a symlink to help Python find the settings module
echo "Creating symlinks for module discovery"
cd ecommerce
ln -sf ecommerce/settings.py settings.py
ls -la
cd ..

# Set environment variable to point to the correct settings module
export DJANGO_SETTINGS_MODULE=ecommerce.settings

# Create symlinks if needed to ensure shop app is accessible
cd ecommerce
python -c "import sys; print(sys.path)"

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Print final structure for debugging
echo "Final directory structure:"
find .. -type d -maxdepth 3 | sort 