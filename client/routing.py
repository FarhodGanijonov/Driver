from django.urls import re_path
from client.consumer import ClientOrderConsumer

# Client websocket url
websocket_urlpatterns = [
    re_path(r'ws/client/$', ClientOrderConsumer.as_asgi())
]
