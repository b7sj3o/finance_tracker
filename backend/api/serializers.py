"""
Serializers for the finance tracker application.
"""

from rest_framework import serializers, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User, Expense, Income, Category


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ["id", "username", "chat_id"]
        # extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create a new user with the given validated data.
        """
        user = User.objects.create_user(
            username=validated_data["username"], chat_id=validated_data["chat_id"]
        )
        return user


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Expense model.
    """

    class Meta:
        model = Expense
        fields = ["id", "amount", "description", "category", "user"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        """
        Create a new income with the given validated data.
        """
        return Expense.objects.create(**validated_data)


class IncomeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Income model.
    """

    class Meta:
        model = Income
        fields = ["id", "amount", "description", "category", "user"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        """
        Create a new income with the given validated data.
        """
        user = validated_data.pop("user")
        return Income.objects.create(user=user, **validated_data)


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "user"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        """
        Create a new income with the given validated data.
        """
        return Category.objects.create(**validated_data)
