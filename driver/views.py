from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from driver.serializers import DriverSerializer
from users.models import AbstractUser

# Driver status update endpoint
class DriverStatusUpdateAPIView(APIView):

    def patch(self, request, driver_id):
        status_value = request.data.get("status")
        driver = AbstractUser.objects.filter(id=driver_id, role="driver").first()

        if not driver:
            return Response({"error": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

        driver.status = status_value

        if status_value == "online":
            driver.is_online = True
        else:
            driver.is_online = False

        driver.save()

        return Response({"message": "Driver status updated"})


# Online driverlar listini ko'rish endpoint
class OnlineDriverListAPIView(APIView):
    def get(self, request):
        drivers = AbstractUser.objects.filter(
            role="driver",
            is_online=True,
            status="idle",
            current_order__isnull=True
        )
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)
