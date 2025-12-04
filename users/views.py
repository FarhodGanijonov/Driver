# users/views.py
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import AbstractUser
from users.serializers import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Utility function for JWT
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Register API
class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, role=None):
        if role not in ['client', 'driver']:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['role'] = role
        serializer = UserRegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            "message": f"{role.capitalize()} registered successfully",
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)


# Login API
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, role=None):
        if role not in ['client', 'driver']:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        try:
            # Role bilan userni aniqlaymiz
            user = AbstractUser.objects.get(phone=phone, role=role)
        except AbstractUser.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Parolni tekshirish
        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Token yaratish
        tokens = get_tokens_for_user(user)

        return Response({
            "message": f"{role.capitalize()} logged in successfully",
            "tokens": tokens,
            "user_id": user.id,
            "role": user.role
        }, status=status.HTTP_200_OK)
