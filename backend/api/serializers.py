"""
Serializers for the finance tracker application.
"""

from rest_framework import serializers
from .models import User, Expense, Income, Category




class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ["id", "username", "chat_id", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create a new user with the given validated data.
        """
        
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
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
