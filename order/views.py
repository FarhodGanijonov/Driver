# orders/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from order.models import Order
from order.serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from order.service import assign_driver


# Order yaratish
class OrderCreateAPIView(APIView):

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        driver = assign_driver(order)

        return Response({
            "order_id": order.id,
            "assigned_driver": driver.full_name if driver else None
        }, status=status.HTTP_201_CREATED)


# Client orderlar ro'yxati
class ClientOrderListAPIView(APIView):
    def get(self, request):
        user = request.user
        status_filter = request.query_params.get("status")
        orders = Order.objects.filter(client=user)
        if status_filter:
            orders = orders.filter(status=status_filter.upper())
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# Orderni tugatish
class OrderCompleteAPIView(APIView):
    def patch(self, request, pk):
        order = Order.objects.filter(id=pk, client=request.user).first()
        if not order:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        order.client_is_finished = True
        order.save()
        return Response({"message": "Order marked as finished"}, status=status.HTTP_200_OK)


# Client order detail endpoint
class ClientOrderDetailAPIView(APIView):
    def get(self, request, pk):
        order = Order.objects.filter(id=pk, client=request.user).first()
        if not order:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


# Client status update endpoint
class ClientStatusUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if request.user.id != pk:
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        status_value = request.data.get("status")
        if status_value not in ["active", "inactive"]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        request.user.status = status_value
        request.user.save()
        return Response({"message": "Client status updated"})


