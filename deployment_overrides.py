"""
Deployment overrides for Django settings.
This file is intended to be imported by Django settings modules to ensure
proper configuration in the Render environment.
"""

import os
import logging

# Set up logging
logging.basicConfig(filename='/tmp/deployment_overrides.log', level=logging.DEBUG)
logging.debug("Loading deployment overrides")

# Override settings for deployment
def apply_render_overrides(settings_module):
    """Apply Render-specific overrides to settings."""
    
    # Always set DEBUG to False in production
    settings_module.DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    logging.debug(f"Set DEBUG to {settings_module.DEBUG}")
    
    # Ensure ALLOWED_HOSTS includes the Render domain
    if not hasattr(settings_module, 'ALLOWED_HOSTS'):
        settings_module.ALLOWED_HOSTS = []
    
    # Add Render domains to ALLOWED_HOSTS
    render_domains = [
        'e-commerce-django-f4um.onrender.com',
        '.onrender.com'
    ]
    
    # Also add any domain from environment variable
    render_host = os.environ.get('ALLOWED_HOSTS', '')
    if render_host and render_host not in render_domains:
        render_domains.append(render_host)
    
    # Add all domains to ALLOWED_HOSTS
    for domain in render_domains:
        if domain not in settings_module.ALLOWED_HOSTS:
            settings_module.ALLOWED_HOSTS.append(domain)
    
    logging.debug(f"Final ALLOWED_HOSTS: {settings_module.ALLOWED_HOSTS}")
    
    return settings_module

# This will be executed when imported
def override_settings():
    """Try to override Django settings."""
    try:
        from django.conf import settings
        apply_render_overrides(settings)
        logging.debug("Successfully applied overrides to Django settings")
    except Exception as e:
        logging.error(f"Error applying overrides: {e}")
        import traceback
        logging.error(traceback.format_exc()) 