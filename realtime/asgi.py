"""
ASGI config for realtime project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from home import consumers
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtime.settings')

ws_patterns = [
    path("ws/pizza/<order_id>/", consumers.OrderProgress),
]

# application = get_asgi_application()

application = ProtocolTypeRouter({
   "websocket": (
        (
            URLRouter(ws_patterns)
        )
    ),
})