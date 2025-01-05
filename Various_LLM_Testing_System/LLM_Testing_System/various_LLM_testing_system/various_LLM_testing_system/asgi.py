"""
ASGI config for various_LLM_testing_system project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Set the default settings module for the Django project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "various_LLM_testing_system.settings")

# Create the ASGI application instance
application = get_asgi_application()
