# client/serializers.py
from rest_framework import serializers
from users.models import AbstractUser


# Clint uchun user serializer
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractUser
        fields = [
            'id',
            'full_name',
            'phone',
            'status',  # active / inactive
            'gender',
            'avatar',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_status(self, value):
        if value not in ['active', 'inactive']:
            raise serializers.ValidationError("Client status must be active or inactive")
        return value
