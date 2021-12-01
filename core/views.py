from chatbot.views import rates, kraken, kraken_price, bittrex, bittrex_price, high_low, check_usd_bitcoin_value, \
    all_prices_loop
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from core.serializers import CurrencySerializer, CategorySerializer, SentimentSerializer
from core.models import Currency, Category
from rest_framework.viewsets import ModelViewSet
import requests
from .models import SentimentData
from django.conf import settings
from django.http import HttpResponse
from twilio.rest import Client

# Metals API
base_currency = 'USD'
symbol = 'XAU'
endpoint = 'latest'
access_key = 'lwx74279m2158ph5vfq2k3m7nbi5yqfox6hz07fmi76qwc9f3w1x2rff1qu6'
get_gold_price = requests.get(
    'https://metals-api.com/api/' + endpoint + '?access_key=' + access_key + '&base=' + base_currency + '&symbols=' + symbol)
latest_gold_price = get_gold_price.json()
latest_gold_price_per_ounce = latest_gold_price['unit']
latest_gold_price_rate_usd_base = latest_gold_price['rates']['USD']
latest_gold_price_rate_ounce_base = latest_gold_price['rates']['XAU']
convert_currencies = requests.get(
    'https://metals-api.com/api/convert?access_key = ' + access_key + '& from = GBP& to = JPY&amount = 25')
converted_result = convert_currencies.json()
user_base_choice = requests.get('https://metals-api.com/api/latest?access_key =' + access_key + '& base = USD')
user_base_choice_result = user_base_choice.json()

# Arbitrage Signal & Latest Rates
arbitrage_signal = high_low()
latest_rate = rates()

# Bitcoin Sentiment API
result = requests.get('https://api.senticrypt.com/v1/bitcoin.json')
get_sentiment = result.json()
mean_sentiment = get_sentiment[-1]['mean']
median_sentiment = get_sentiment[-1]['median']
rate = get_sentiment[-1]['rate']
if median_sentiment > mean_sentiment and rate > 1:
    message = 'The Sentiment is Positive. Buy Bitcoin'
else:
    message = 'The Sentiment is Negative. Sell Bitcoin'


def home(request):
    return render(request, "index.html", {
        "sell_bitcoin_thresh": 102000,
        "bitcoin_price": bittrex_price,
        "sentiment": mean_sentiment,
        "sentiment_message": message,
        "arbitrage_signal": arbitrage_signal,
        "latest_rates": latest_rate,
        "latest_gold_price": latest_gold_price,
        "latest_unit": latest_gold_price_per_ounce,
        "latest_rate": latest_gold_price_rate_usd_base,
        "latest_rate_per_ounce_base": latest_gold_price_rate_ounce_base,
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


# Daily sending subscribers some signals.
def broadcast_sms(request):
    message_to_broadcast = (f"This is your daily Bitcoin Sentiment Message. {message}. "
                            f"The rate is @ {rate} and the mean is @ {mean_sentiment}"
                            f" Arbitraging opportunity:  {arbitrage_signal} ")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
        if recipient:
            client.messages.create(to=recipient,
                                   # messaging_service_sid='MG17ddcf9a439835d83e589a8f3275c5e7',
                                   # from_='+16106461582',
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)
    return HttpResponse(f"messages sent to recipients. ", recipient, 200)
