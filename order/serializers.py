from django.contrib.gis.geos import Point
from rest_framework import serializers
from .models import Order

# Order serializer
class OrderSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    driver_name = serializers.CharField(source='driver.full_name', read_only=True)
    pickup_point = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "client",
            "client_name",
            "driver",
            "driver_name",
            "status",
            "description",
            "gender",
            "location",
            "pickup_point",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["status", "client", "driver", "client_name", "driver_name", "created_at", "updated_at"]

    def get_pickup_point(self, obj):
        if obj.location:
            return {"lat": obj.location.y, "lon": obj.location.x}
        return None

    def create(self, validated_data):
        # Client ni request.user qilib qo'yish
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['client'] = request.user

        # Agar location berilgan bo'lsa, Point obyekti yaratish
        location_data = validated_data.pop("location", None)
        if location_data and "coordinates" in location_data:
            coords = location_data["coordinates"]
            validated_data["location"] = Point(coords[0], coords[1])

        return super().create(validated_data)

