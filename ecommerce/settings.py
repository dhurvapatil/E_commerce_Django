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
    
    # Check for settings.py in ecommerce directory
    ecommerce_dir_contents = os.listdir(ecommerce_dir)
    logging.debug(f"ecommerce directory contents: {ecommerce_dir_contents}")
    
    if 'settings.py' in ecommerce_dir_contents:
        logging.debug("Found settings.py in ecommerce directory")
        
        # Import all settings from the inner settings module
        try:
            sys.path.insert(0, ecommerce_dir)
            from ecommerce.settings import *
            logging.debug("Successfully imported settings from ecommerce.settings")
        except ImportError as e:
            logging.error(f"Error importing from ecommerce.settings: {str(e)}")
            raise
    else:
        logging.error("No settings.py found in ecommerce directory")
        raise FileNotFoundError("No settings.py found in ecommerce directory")
else:
    logging.error("No ecommerce directory found")
    raise FileNotFoundError("No ecommerce directory found") 