from django.urls import path
from .views import DriverStatusUpdateAPIView, OnlineDriverListAPIView

urlpatterns = [
    # Driver statusni o'zi boshqarishi uchun url
    path("<int:pk>/status/", DriverStatusUpdateAPIView.as_view()),

    # Client online driverlar listini korish uchun url
    path("online/", OnlineDriverListAPIView.as_view()),
]
