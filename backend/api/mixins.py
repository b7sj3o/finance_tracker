from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# from rest_framework_simplejwt.authentication import JWTAuthentication

CONTENT_TYPE_JSON = "application/json"


class UserFilteredMixin(generics.GenericAPIView):
    """
    Mixin to filter queryset by the current user.
    """

    def get_queryset(self):
        """
        Returns the queryset filtered by the current user.
        """
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Saves the serializer with the current user.
        """
        serializer.save(user=self.request.user)


class ContentTypeValidationMixin:
    """
    Mixin to validate Content-Type header for JSON requests.
    """

    def validate_content_type(self, request):
        """
        Validates that the Content-Type header is application/json.
        """
        if request.content_type != CONTENT_TYPE_JSON:
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )
        return None


class ListMixin:
    """
    Mixin to handle GET requests for listing objects.
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to list objects.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateMixin:
    """
    Mixin to handle POST requests for creating new objects.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create new objects.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveMixin:
    """
    Mixin to handle GET requests for retrieving a single object.
    """

    def get_object(self, pk):
        """
        Retrieves the object by primary key and ensures it belongs to the current user.
        """
        return get_object_or_404(self.get_queryset(), pk=pk)

    def get(self, request, pk, *args, **kwargs):
        """
        Handles GET requests to retrieve a single object.
        """
        obj = self.get_object(pk)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateMixin:
    """
    Mixin to handle PUT and PATCH requests for updating objects.
    """

    def put(self, request, pk, *args, **kwargs):
        """
        Handles PUT requests to update an object.
        """
        obj = self.get_object(pk)
        serializer = self.get_serializer(obj, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        """
        Handles PATCH requests to partially update an object.
        """
        obj = self.get_object(pk)
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteMixin:
    """
    Mixin to handle DELETE requests for removing objects.
    """

    def delete(self, request, pk, *args, **kwargs):
        """
        Handles DELETE requests to remove an object.
        """
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
