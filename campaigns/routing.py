from django.urls import re_path
from .consumers import ParticipantConsumer

websocket_urlpatterns = [
    re_path(r'participant/$', ParticipantConsumer.as_asgi()),
]
