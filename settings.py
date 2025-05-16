"""
Django settings for ecommerce project.
This is a standalone settings file to be used on Render.
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(filename='/tmp/settings_debug.log', level=logging.DEBUG)
logging.debug("Loading standalone settings file")

# Import load_env to set environment variables
try:
    import load_env
    logging.debug("Loaded environment variables from load_env.py")
except Exception as e:
    logging.error(f"Error loading environment variables: {e}")

# Build paths inside the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.debug(f"BASE_DIR: {BASE_DIR}")

# Add BASE_DIR to Python path
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Add ecommerce directory to Python path
ecommerce_dir = os.path.join(BASE_DIR, 'ecommerce')
if ecommerce_dir not in sys.path:
    sys.path.insert(0, ecommerce_dir)
    logging.debug(f"Added ecommerce directory to sys.path: {ecommerce_dir}")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ya9)sxab8qj*%7@o^%406d_f6w-_e90e@u2ovh0gu-p#(3%*f0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
logging.debug(f"DEBUG: {DEBUG}")

# ALLOWED_HOSTS - explicitly add the Render domain
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'e-commerce-django-f4um.onrender.com', '.onrender.com']
render_host = os.environ.get('ALLOWED_HOSTS', '')
if render_host and render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_host)
logging.debug(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'
logging.debug(f"ROOT_URLCONF set to: {ROOT_URLCONF}")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'
logging.debug(f"WSGI_APPLICATION set to: {WSGI_APPLICATION}")

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'ecommerce', 'db.sqlite3'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'ecommerce', 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'ecommerce', 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'ecommerce', 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URLs
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Apply deployment overrides
try:
    import deployment_overrides
    deployment_overrides.override_settings()
    logging.debug("Applied deployment overrides")
except Exception as e:
    logging.error(f"Error applying deployment overrides: {e}")

# Make sure ALLOWED_HOSTS is properly set after importing inner settings
if 'e-commerce-django-f4um.onrender.com' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('e-commerce-django-f4um.onrender.com')
if '.onrender.com' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('.onrender.com')

# Print the final ALLOWED_HOSTS for debugging
logging.debug(f"Final ALLOWED_HOSTS: {ALLOWED_HOSTS}") 