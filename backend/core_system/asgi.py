"""
ASGI config for core_system project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import hse_module.hse_pob.routing
import hse_module.hse_ptw.routing
import hse_module.hse_safety.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_system.settings')

# Combine all WebSocket URL patterns
websocket_routes = (
    hse_module.hse_pob.routing.websocket_urlpatterns +
    hse_module.hse_ptw.routing.websocket_urlpatterns +
    hse_module.hse_safety.routing.websocket_urlpatterns
)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_routes
        )
    ),
})