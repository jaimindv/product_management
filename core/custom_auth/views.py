from django.contrib.auth import authenticate, login, logout
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from base.permissions import IsAPIKeyAuthenticated
from core.custom_auth.models import User

from .serializers import (
    LoginSerializer,
    RegisterUserSerializer,
)


class RegisterView(views.APIView):
    authentication_classes = []
    permission_classes = [IsAPIKeyAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User registered successfully.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class LoginView(views.APIView):
    authentication_classes = []
    permission_classes = [IsAPIKeyAuthenticated]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        if not User.objects.filter(email=email).exists():
            return Response(
                {
                    "error": "Invalid email.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            # JWT token
            refresh_token = RefreshToken.for_user(user)
            response = {
                "message": "Login Successfully",
                "user_id": user.id,
                "email": user.email,
                "refresh_token": str(refresh_token),
                "access_token": str(refresh_token.access_token),
            }
            return Response(data=response)
        else:
            return Response(
                {
                    "error": "Incorrect password.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(views.APIView):

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            # Blacklist token
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response(
                {"message": "Logout successful."}, status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"error": "Invalid or already Blacklisted Refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UpdateUserView(views.APIView):
    # authentication_classes = []
    # permission_classes = [IsAPIKeyAuthenticated]

    def patch(self, request, *args, **kwargs):
        instance = request.user
        serializer = RegisterUserSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(
            {"message": "User updated successfully.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
