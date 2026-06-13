from rest_framework import serializers

from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "user", "name", "description", "monthly_limit"]


class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Expense
        fields = ["id", "user", "title", "amount", "currency", "category", "date", "notes"]