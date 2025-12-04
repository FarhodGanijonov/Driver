# users/urls.py
from django.urls import path
from users.views import UserRegisterAPIView, UserLoginAPIView

urlpatterns = [
    # Register driver or client
    path('register/<str:role>/', UserRegisterAPIView.as_view(), name='user-register'),

    # Login driver or client
    path('login/<str:role>/', UserLoginAPIView.as_view(), name='user-login'),
]
