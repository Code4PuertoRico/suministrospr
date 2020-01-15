"""
WSGI config for suministrospr project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""
import os

from configurations.wsgi import get_wsgi_application

configuration = os.getenv("ENVIRONMENT", "development").title()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suministrospr.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", configuration)


application = get_wsgi_application()
