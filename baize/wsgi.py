"""
WSGI config for baize project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from utils import share_memory
from core.spider_engine import SpiderEngine

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baize.settings")

application = get_wsgi_application()

share_memory.spider_engine = SpiderEngine()

