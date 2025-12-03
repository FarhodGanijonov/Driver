from rest_framework import serializers
from .models import Order

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
        read_only_fields = ["status", "driver", "client_name", "driver_name", "created_at", "updated_at"]

    def get_pickup_point(self, obj):
        if obj.location:
            return {"lat": obj.location.y, "lon": obj.location.x}
        return None
