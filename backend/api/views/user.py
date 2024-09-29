"""
Views for handling API requests for all the stuff with user.
"""

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from django.contrib.auth import login

from ..models import User
from ..serializers import (
    UserSerializer,
)
from ..mixins import (
    ContentTypeValidationMixin,
)


class UserCreateView(ContentTypeValidationMixin, generics.CreateAPIView):
    """
    Create a new user with content type validation.
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        login(request, user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetUserView(generics.RetrieveAPIView):
    # def get(self, request, *args, **kwargs):
    #     serializer = UserSerializer(request.user)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    queryset = User.objects.all()
    serializer_class = UserSerializer
