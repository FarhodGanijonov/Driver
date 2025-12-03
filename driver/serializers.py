# driver/serializers.py
from rest_framework import serializers
from users.models import AbstractUser


# Clint uchun user serializer
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractUser
        fields = [
            'id',
            'full_name',
            'phone',
            'status',
            'gender',
            'avatar',
            'created_at',
            'point',        # driver joylashuvi
            'current_order', # agar driver band bo'lsa
        ]
        read_only_fields = ['id', 'created_at', 'point', 'current_order']

    def get_user_point(self, obj):
        return {'lat': obj.user.point.y, 'lon': obj.user.point.x}


    def validate_status(self, value):
        if value not in ['idle', 'online', 'busy']:
            raise serializers.ValidationError("Driver status must be idle, online, or busy")
        return value


