from rest_framework import serializers

from core.models import Currency, Category, SentimentData


class SentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentData
        fields = ("id", "rate", "count", "mean", "median", "sum", "date_time", "btc_price", "comment")


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")
