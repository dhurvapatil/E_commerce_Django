#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

# Set up logging
logging.basicConfig(filename='/tmp/manage_inner_debug.log', level=logging.DEBUG)
logging.debug("Starting management command from inner manage.py")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    
    # Explicitly set ALLOWED_HOSTS in environment variables
    if 'ALLOWED_HOSTS' not in os.environ:
        os.environ['ALLOWED_HOSTS'] = 'e-commerce-django-f4um.onrender.com,.onrender.com'
        logging.debug("Set ALLOWED_HOSTS environment variable")
    
    # Set DEBUG to False in production
    if 'DEBUG' not in os.environ:
        os.environ['DEBUG'] = 'False'
    
    # Log the environment variables
    logging.debug(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    logging.debug(f"ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS')}")
    logging.debug(f"DEBUG: {os.environ.get('DEBUG')}")
    
    # Log the current directory and Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logging.debug(f"Current directory: {current_dir}")
    logging.debug(f"Python path: {sys.path}")
    
    # Add the current directory to sys.path if needed
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        logging.debug(f"Added current directory to sys.path: {current_dir}")
    
    try:
        from django.core.management import execute_from_command_line
        logging.debug(f"Successfully imported Django management command")
        
        # Try to directly modify ALLOWED_HOSTS
        try:
            from django.conf import settings
            if hasattr(settings, 'ALLOWED_HOSTS'):
                if 'e-commerce-django-f4um.onrender.com' not in settings.ALLOWED_HOSTS:
                    settings.ALLOWED_HOSTS.append('e-commerce-django-f4um.onrender.com')
                if '.onrender.com' not in settings.ALLOWED_HOSTS:
                    settings.ALLOWED_HOSTS.append('.onrender.com')
                logging.debug(f"Updated ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        except Exception as e:
            logging.error(f"Error updating ALLOWED_HOSTS: {e}")
        
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        logging.error(f"Error importing Django: {exc}")
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    except Exception as e:
        logging.error(f"Error executing management command: {e}")
        raise


if __name__ == '__main__':
    main()
