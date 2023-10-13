"""
WSGI config for market project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
load_dotenv()  # loads the configs from .env

from django.core.wsgi import get_wsgi_application

DJANGO_SETTINGS_MODULE = str(os.getenv("DJANGO_SETTINGS_MODULE"))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_SETTINGS_MODULE)

application = get_wsgi_application()
