from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login as auth_login
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer, LoginSerializer
import logging

logger = logging.getLogger(__name__)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "User created successfully",
                    "user": UserSerializer(username).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            auth_login(request, user)

            response_data = {
                "user": {
                    "username": user.username,
                }
            }

            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(key='sessionid', value=request.session.session_key, httponly=True, samesite='Lax')
            return response
        
        logger.error('Login error: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def expnses():
    pass


def income():
    pass


def profiles():
    pass

