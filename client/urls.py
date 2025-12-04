from django.urls import path
from .views import (OrderCreateAPIView, ClientOrderListAPIView,
                    ClientOrderDetailAPIView,
                    ClientStatusUpdateAPIView
)

urlpatterns = [
    #Client order create api
    path("order/create/", OrderCreateAPIView.as_view(), name="order-create"),

    # Client order list va list filter status EXAMPLE: "?status=completed"
    path("order/list/", ClientOrderListAPIView.as_view(), name="order-list"),

    # Client order detail get
    path("orders/<int:pk>/", ClientOrderDetailAPIView.as_view(), name="client-order-detail"),

    # Client o'zini statusini update qilishi mumkin faqat "active/inactive" ga update qila oladi
    path("<int:pk>/status/", ClientStatusUpdateAPIView.as_view(), name="client-status-update"),

]
