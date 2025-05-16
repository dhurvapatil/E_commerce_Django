"""
Root URL configuration for ecommerce project.
"""

import logging
import os

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

logging.basicConfig(filename='/tmp/urls_debug.log', level=logging.DEBUG)
logging.debug("Loading root urls.py")

# Add static and media URLs in debug mode
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]

# Add static and media URLs
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Even in production, serve media files directly for this demo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

logging.debug(f"Final urlpatterns: {urlpatterns}") 