#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    
    # Add the current directory to sys.path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Add the shop app directory to sys.path if needed
    shop_dir = os.path.join(current_dir, 'ecommerce', 'shop')
    if os.path.exists(shop_dir) and shop_dir not in sys.path:
        sys.path.insert(0, shop_dir)
    
    # Explicitly set ALLOWED_HOSTS in case it's not being picked up from settings
    import django
    from django.conf import settings
    if hasattr(settings, 'ALLOWED_HOSTS'):
        if 'e-commerce-django-f4um.onrender.com' not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS.append('e-commerce-django-f4um.onrender.com')
        if '.onrender.com' not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS.append('.onrender.com')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main() 