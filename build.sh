#!/usr/bin/env bash
# exit on error
set -o errexit

# Print the directory structure for debugging
echo "Directory structure before setup:"
find . -type d -maxdepth 3 | sort

# Make sure the static directories exist
echo "Creating necessary directories"
mkdir -p static
mkdir -p ecommerce/static
mkdir -p ecommerce/staticfiles

# Install dependencies
echo "Installing dependencies"
pip install django pillow gunicorn

# Update inner ecommerce settings to ensure ALLOWED_HOSTS is set
echo "Updating ecommerce/ecommerce/settings.py to set ALLOWED_HOSTS"
RENDER_HOST="e-commerce-django-f4um.onrender.com"
if grep -q "ALLOWED_HOSTS" ecommerce/ecommerce/settings.py; then
    sed -i "s/ALLOWED_HOSTS = \[[^]]*\]/ALLOWED_HOSTS = ['localhost', '127.0.0.1', '$RENDER_HOST', '.onrender.com']/" ecommerce/ecommerce/settings.py
    echo "Updated ALLOWED_HOSTS in ecommerce/ecommerce/settings.py"
fi

# Set environment variables for the build process
export DJANGO_SETTINGS_MODULE=ecommerce.ecommerce.settings
export ALLOWED_HOSTS="$RENDER_HOST,.onrender.com"
export DEBUG=False

echo "Environment variables set:"
echo "DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE"
echo "ALLOWED_HOSTS=$ALLOWED_HOSTS"
echo "DEBUG=$DEBUG"

# Apply migrations directly with the inner ecommerce settings
echo "Applying migrations..."
cd ecommerce
python manage.py migrate --settings=ecommerce.settings

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=ecommerce.settings
cd ..

# Print final structure for debugging
echo "Final directory structure:"
find . -type d -maxdepth 3 | sort 