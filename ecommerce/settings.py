"""
This settings file acts as a bridge to the actual settings module.
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

# Print dir contents for debugging
dir_contents = os.listdir(current_dir)
logging.debug(f"Directory contents: {dir_contents}")

# Check for ecommerce directory
if 'ecommerce' in dir_contents and os.path.isdir(os.path.join(current_dir, 'ecommerce')):
    ecommerce_dir = os.path.join(current_dir, 'ecommerce')
    logging.debug(f"Found ecommerce directory: {ecommerce_dir}")
    
    # Add ecommerce dir to sys.path
    if ecommerce_dir not in sys.path:
        sys.path.insert(0, ecommerce_dir)
        
    # Check for settings.py in ecommerce directory
    ecommerce_dir_contents = os.listdir(ecommerce_dir)
    logging.debug(f"ecommerce directory contents: {ecommerce_dir_contents}")
    
    if 'settings.py' in ecommerce_dir_contents:
        logging.debug("Found settings.py in ecommerce directory")
        
        # Import directly from the module, not as a relative import
        try:
            # Import the inner settings module
            inner_settings = os.path.join(ecommerce_dir, 'settings.py')
            logging.debug(f"Importing from {inner_settings}")
            
            # Execute the settings file directly
            with open(inner_settings) as f:
                exec(f.read())
                
            logging.debug("Successfully imported settings via exec")
            logging.debug(f"ROOT_URLCONF is set to: {locals().get('ROOT_URLCONF', 'Not found')}")
            
            # To verify settings are loaded
            for key in ['DEBUG', 'INSTALLED_APPS', 'ROOT_URLCONF', 'DATABASES']:
                logging.debug(f"Setting {key}: {locals().get(key, 'Not found')}")
                
        except Exception as e:
            logging.error(f"Error importing settings via exec: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            raise
    else:
        logging.error("No settings.py found in ecommerce directory")
        raise FileNotFoundError("No settings.py found in ecommerce directory")
else:
    logging.error("No ecommerce directory found")
    raise FileNotFoundError("No ecommerce directory found")

# Define default settings if they're missing
if 'ROOT_URLCONF' not in locals():
    ROOT_URLCONF = 'ecommerce.urls'
    logging.debug(f"Set default ROOT_URLCONF to {ROOT_URLCONF}") 