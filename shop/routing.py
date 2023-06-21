from django.urls import re_path
from .consumers import RestockConsumer

websocket_urlpatterns = [
    re_path(r'ws/restock/$', RestockConsumer.as_asgi()),
]
