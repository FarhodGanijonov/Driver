from django.urls import re_path
from client.consumer import ClientOrderConsumer

websocket_urlpatterns = [
    re_path(r'ws/client/(?P<client_id>\d+)/$', ClientOrderConsumer.as_asgi())
]
