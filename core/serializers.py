from rest_framework import serializers

from core.models import Currency, Category, SentimentData


class SentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentData
        fields = ("id", "rate", "polarity", "mean", "median", "date_time", "btc_price")


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")
