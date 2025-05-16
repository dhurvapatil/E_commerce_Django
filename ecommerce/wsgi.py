"""
WSGI config for ecommerce project.

This file imports the original WSGI application from the ecommerce/ subdirectory.
"""

import os
import sys

# Add the project directory to the Python path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

from ecommerce.wsgi import application  # Import the application from the inner ecommerce directory 