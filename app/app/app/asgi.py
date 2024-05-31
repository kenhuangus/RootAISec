"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
application = get_asgi_application()

from app.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

ws_app = URLRouter(websocket_urlpatterns)
ws_app = AuthMiddlewareStack(ws_app)

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": application,

    # WebSocket chat handler
    'websocket': ws_app
})