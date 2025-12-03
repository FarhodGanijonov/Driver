from django.urls import path
from .views import OrderCreateAPIView, ClientOrderListAPIView, OrderCompleteAPIView, ClientOrderDetailAPIView, \
    ClientStatusUpdateAPIView

urlpatterns = [
    path("order/create/", OrderCreateAPIView.as_view(), name="order-create"),
    path("order/list/", ClientOrderListAPIView.as_view(), name="order-list"),
    path("order/<int:pk>/complete/", OrderCompleteAPIView.as_view(), name="order-complete"),
    path("orders/<int:pk>/", ClientOrderDetailAPIView.as_view(), name="client-order-detail"),
    path("<int:pk>/status/", ClientStatusUpdateAPIView.as_view(), name="client-status-update"),

]
