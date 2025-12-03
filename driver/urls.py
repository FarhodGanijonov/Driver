from django.urls import path
from .views import DriverStatusUpdateAPIView, OnlineDriverListAPIView

urlpatterns = [
    path("<int:pk>/status/", DriverStatusUpdateAPIView.as_view()),
    path("online/", OnlineDriverListAPIView.as_view()),
]
