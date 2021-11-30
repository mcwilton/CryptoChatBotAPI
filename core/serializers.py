from rest_framework import serializers

from core.models import Currency, Category

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields= ("id", "code", "name")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields= ("id", "name")
