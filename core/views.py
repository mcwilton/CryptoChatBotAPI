import datetime
from chatbot.views import rates, kraken, kraken_price, bittrex, bittrex_price, hilow, check_usd_bitcoin_value, \
    all_prices_loop
from alphavantage.price_history import API_KEY
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import loader
from rest_framework.generics import ListAPIView
from core.serializers import CurrencySerializer, CategorySerializer, SentimentSerializer
from core.models import Currency, Category
from rest_framework.viewsets import ModelViewSet
import requests
from .models import SentimentData
import ccxt
from django.conf import settings
from django.http import HttpResponse
from twilio.rest import Client

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
user_base_choice = requests.get('https://metals-api.com/api/latest?access_key =' + access_key + '& base = USD')
user_base_choice_result = user_base_choice.json()


result = requests.get('https://api.senticrypt.com/v1/bitcoin.json')
get_sentiment = result.json()
mean_sentiment = get_sentiment[-1]['mean']
median_sentiment = get_sentiment[-1]['median']
rate = get_sentiment[-1]['rate']
if median_sentiment > mean_sentiment and rate > 1:
    message = 'The Sentiment is Positive. Buy Bitcoin'
else:
    message = 'The Sentiment is Negative. Sell Bitcoin'


def get_sentiment_data(request):
    pass
#     # all_data = {}
#     url = 'https://api.senticrypt.com/v1/bitcoin.json'
#     response = requests.get(url)
#     data = response.json()
#     # print(data)
#     sentiment = data[-1]
#
#     for i in sentiment:
#         sentiment_data = SentimentData(
#             rate=i[float('rate')],
#             count=i['count'],
#             median=i['median'],
#             mean=i['mean'],
#             ####################polarity=i['polarity'],
#             sum=i['sum'],
#             btc_price=i['btc_price'],
#             date_time=i['date_time']
#         )
#         sentiment_data.save()
#         all_sentiment_data = SentimentData.objects.all().order_by('-id')
#     # html = "<html><body> It is now %s.</body></html>"% all_sentiment_data
#
#     # return HttpResponse()


def index(request):

    return render(request, "index.html", {
        "sell_bitcoin_thresh": 102000,
        "bitcoin_price": bittrex_price,
        "sentiment": mean_sentiment,
        "sentiment_message": message,
    })


class SentimentModelViewSet(ModelViewSet):
    queryset = SentimentData.objects.all()
    serializer_class = SentimentSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def broadcast_sms(request):
    message_to_broadcast = (f"This is your daily Bitcoin Sentiment Message. {message}. "
                            f"The rate is @ {rate} and the mean is @ {mean_sentiment}")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
        if recipient:
            client.messages.create(to=recipient,
                                   # messaging_service_sid='MG17ddcf9a439835d83e589a8f3275c5e7',
                                   # from_='+16106461582',
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)
    return HttpResponse("messages sent to: ", recipient, 200)
