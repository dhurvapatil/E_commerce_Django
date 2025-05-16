"""
Root URL configuration for ecommerce project.
This simply forwards to the inner ecommerce.urls module.
"""

from django.urls import path, include

urlpatterns = [
    path('', include('ecommerce.urls')),
] 