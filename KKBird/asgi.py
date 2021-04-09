"""
ASGI config for KKBird project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import re_path

from model_detection.views import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KKBird.settings')

django.setup()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/chat/$', ChatConsumer.as_asgi()),
        ])
    ),
})
