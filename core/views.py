from rest_framework.generics import ListAPIView
from core.serializers import CurrencySerializer, CategorySerializer
from core.models import Currency, Category
from rest_framework.viewsets import ModelViewSet
import requests
from .models import SentimentData


def get_sentiment_data(request):
    # all_data = {}
    url = 'https://api.senticrypt.com/v1/bitcoin.json'
    response = requests.get(url)
    data = response.json()
    # print(data)
    sentiment = data[-1]

    for i in sentiment:
        sentiment_data = SentimentData(
            rate=i['rate'],
            count=i['count'],
            median=i['median'],
            mean=i['mean'],
            polarity=i['polarity'],
            sum=i['sum'],
            bitcoin_price=i['bitcoin_price'],
            date_time=i['date_time'],
        )
        sentiment_data.save()
        all_sentiment_data = SentimentData.objects.all().order_by('-id')


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
