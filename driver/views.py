from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from driver.serializers import DriverSerializer
from users.models import AbstractUser

# Driver status update endpoint
class DriverStatusUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        status_value = request.data.get("status")
        driver = AbstractUser.objects.filter(id=pk, role="driver").first()

        if not driver:
            return Response({"error": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

        # Faqat ruxsat berilgan statuslar
        allowed = ["online", "offline", "busy"]
        if status_value not in allowed:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        # Agar driver band bo'lsa busy statusni o'zgartirib bo'lmaydi
        if driver.status == "busy" and status_value in ["offline"]:
            return Response({"error": "Cannot change status while driver is busy with an order"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Statusni yangilash
        driver.status = status_value
        driver.is_online = (status_value == "online")
        driver.save()

        return Response({"message": f"Status changed to {status_value}"})


# Online driverlar listini ko'rish endpoint
class OnlineDriverListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        drivers = AbstractUser.objects.filter(
            role="driver",
            is_online=True,
            status="online",
            current_order__isnull=True
        )
        # print(drivers)
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)
