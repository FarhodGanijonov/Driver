from django.urls import re_path
from driver.consumer import DriverConsumer

# Driver websocket url
websocket_urlpatterns = [
    re_path(r"ws/driver/$", DriverConsumer.as_asgi()),
]
