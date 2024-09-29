"""
Views for handling API requests for models and doing CRUD.
"""

from rest_framework import status, generics, mixins
from rest_framework.response import Response

from ..models import Expense, Income, Category
from ..serializers import (
    ExpenseSerializer,
    IncomeSerializer,
    CategorySerializer,
)
from ..mixins import (
    ContentTypeValidationMixin,
)


class BaseCRUDView(
    ContentTypeValidationMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    Base CRUD View for executing simple operations described in CRUD

    required fields:
    queryset = *Model*.objects.all()
    serializer_class = *ModelSerializer*
    """

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        print(request.user)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.create(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.update(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.partial_update(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if "pk" in kwargs:
            self.destroy(request, *args, **kwargs)
            return Response({"message": "Item was deleted"}, status=status.HTTP_200_OK)
        return self.list(request, *args, **kwargs)


class ExpenseView(BaseCRUDView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def post(self, request, *args, **kwargs):
        amount = float(request.data.get("amount"))
        if request.user.balance - amount < 0:
            return Response(
                data={
                    "message": "You don't have enough balance to perform this operation"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        request.user.update_balance()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IncomeView(BaseCRUDView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        request.user.update_balance()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryView(BaseCRUDView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
