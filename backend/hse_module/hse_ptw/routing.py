from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/ptw_updates/$', consumers.PTWConsumer.as_asgi()),
]
