"""
Views for handling API requests for all the stuff with user.
"""

from rest_framework import generics
from rest_framework.permissions import AllowAny

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


class GetUserView(generics.RetrieveAPIView):
    # def get(self, request, *args, **kwargs):
    #     serializer = UserSerializer(request.user)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    queryset = User.objects.all()
    serializer_class = UserSerializer
