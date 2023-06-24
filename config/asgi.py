from channels.routing import ProtocolTypeRouter, URLRouter
from chat.channelsmiddleware import TokenAuthMiddleware
import campaigns.routing
import chat.routing
import shop.routing
import alarms.routing
import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': TokenAuthMiddleware(
        URLRouter(
            chat.routing.websocket_urlpatterns +
            shop.routing.websocket_urlpatterns +
            campaigns.routing.websocket_urlpatterns +
            alarms.routing.websocket_urlpatterns
        )
    ),
})
