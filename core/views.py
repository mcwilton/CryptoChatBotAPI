from alphavantage.price_history import API_KEY
from rest_framework.generics import ListAPIView
from core.serializers import CurrencySerializer, CategorySerializer, SentimentSerializer
from core.models import Currency, Category
from rest_framework.viewsets import ModelViewSet
import requests
from .models import SentimentData
import ccxt

base_currency = 'USD'
symbol = 'XAU'
endpoint = 'latest'
access_key = '2m95urdhuj4wpwilv2hwv1gz365j8s543y9uysw23zy7y2r8uycsi6va4z99'
get_gold_price = requests.get(
    'https://metals-api.com/api/' + endpoint + '?access_key=' + access_key + '&base=' + base_currency + '&symbols=' + symbol)
latest_gold_price = get_gold_price.json()
convert_currencies = requests.get(
    'https://metals-api.com/api/convert?access_key = ' + access_key + '& from = GBP& to = JPY&amount = 25')
converted_result = convert_currencies.json()
user_base_choice = requests.get('https://metals-api.com/api/latest?access_key =' + access_key+'& base = USD')
user_base_choice_result = user_base_choice.json()


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
            btc_price=i['btc_price'],
            date_time=i['date_time']
        )
        sentiment_data.save()
        all_sentiment_data = SentimentData.objects.all().order_by('-id')


class SentimentModelViewSet(ModelViewSet):
    queryset = SentimentData.objects.all()
    serializer_class = SentimentSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
