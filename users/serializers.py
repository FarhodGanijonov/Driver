from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import AbstractUser

# Client va Driver uchun register serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = AbstractUser
        fields = ['phone', 'full_name', 'password', 'password2', 'role']

    def validate(self, attrs):
        # Passwordlar mosligini tekshirish
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # Shu telefon va rol bo‘yicha user mavjudligini tekshirish
        if AbstractUser.objects.filter(phone=attrs['phone'], role=attrs['role']).exists():
            raise serializers.ValidationError({
                "phone": f"User with phone {attrs['phone']} and role {attrs['role']} already exists."
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        role = validated_data['role']

        # Role ga qarab default status beramiz
        if role == 'driver':
            validated_data['status'] = 'idle'
        elif role == 'client':
            validated_data['status'] = 'active'

        user = AbstractUser.objects.create_user(
            phone=validated_data['phone'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            role=role,
            status=validated_data['status']
        )
        return user

# Client va Driver userlar uchun login serializer
class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
