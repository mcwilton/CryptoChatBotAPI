from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import datetime
import math
import emoji
import time
import re
import ccxt
import requests
import cryptocompare
from forex_python.bitcoin import BtcConverter
from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes
from blockcypher import get_address_overview

bitmex = ccxt.bitmex()
bittrex = ccxt.bittrex()
kraken = ccxt.kraken()

bitmex_price = f"Bitmex for $ {bitmex.fetch_ticker('BTC/USD')['close']}"
bittrex_price = f"Bittrex for $ {bittrex.fetch_ticker('BTC/USD')['close']}"
kraken_price = f"Kraken for $ {kraken.fetch_ticker('BTC/USD')['close']}"

all_prices_loop = [bitmex_price, bittrex_price, kraken_price]


def hilow():
    highest_price = max(all_prices_loop)
    lowest_price = min(all_prices_loop)
    arbitrage_high = highest_price.split()[3]
    arbitrage_low = lowest_price.split()[3]
    arbitrage = float(arbitrage_high) - float(arbitrage_low)
    return f"Buy on {lowest_price} and sell on {highest_price}. Your arbitrage gain is ${round(arbitrage, 2)}"


def rates():
    current_price = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    json_data = current_price.json()
    return f"Bitcoin to top 3 global currencies \n" \
           f" \n" \
           f"USD - ${str(json_data['bpi']['USD']['rate_float'])} \n" \
           f"EUR - E{str(json_data['bpi']['EUR']['rate_float'])} \n" \
           f"GBP - G{str(json_data['bpi']['GBP']['rate_float'])} \n"


def check_usd_bitcoin_value(amount):
    validate = requests.get(f"https://blockchain.info/tobtc?currency=USD&value={amount}")
    data = validate.json()
    return data


@csrf_exempt
def index(request):
    if request.method == 'POST':

        incoming_msg = request.POST['Body'].lower()
        message = incoming_msg.split()

        resp = MessagingResponse()
        msg = resp.message()
        responded = False

        if 'hi' in incoming_msg:
            reply = emoji.emojize("""
Welcome to BitBot. For everything bitcoin.
Select a number like 1 or type a word like 'bitcoin'
\n
*1 :* Check the Arbitrage Algorithm Signal.
\n
*2 :* Check the EUR, USD & GBP to Bitcoin prices.
\n
*3 :* Check the ZAR, TZS, KSH, GHC, NGN to Bitcoin prices.
\n
*convert :* Convert usd to bitcoin. eg convert 5000 usd to bitcoin
\n
*check date:* Check date for bitcoins value eg usd check date 2 bitcoins on 12.12.2015
\n
*get address:* Get a new bitcoin address type 'get address'
\n
*latest :* Get the latest B price to any currency eg latest 3 bitcoins to zar
\n
*news :* Get the latest Bitcoin News
\n
*qrcode :* get a QR Code for your Bitcoin address


                """, use_aliases=True)
            msg.body(reply)
            responded = True

        elif incoming_msg == '1':
            reply = hilow()
            msg.body(str(reply))
            responded = True

        elif incoming_msg == '2':
            reply = rates()
            msg.body(str(reply))
            responded = True

        elif incoming_msg == '3':
            reply = cryptocompare.get_price(['BTC'], ['ZAR', 'NGN', 'KES', 'GHC', 'TZS'])
            msg.body(str((f"Bitcoin to top 5 African countries \n"
                          f"\n"
                          f"BTC to SA Rand is R{reply['BTC']['ZAR']} \n"
                          f"BTC to Ng Naira is N{reply['BTC']['NGN']} \n"
                          f"BTC to Gh Shillings is G{reply['BTC']['GHC']} \n"
                          f"BTC to Ky Shillings is K{reply['BTC']['KES']} \n"
                          f"BTC to Tz Shillings is T{reply['BTC']['TZS']} \n"
                          )))
            responded = True

        # convert 5000 usd to bitcoin
        elif 'convert' in incoming_msg:
            amount = float(re.search(r'\d+', incoming_msg).group(0))
            reply = check_usd_bitcoin_value(amount)
            msg.body(f"USD{amount} converted to Bitcoin is B{str(reply)}")
            responded = True

        # qrcode 1M5m1DuGw4Wyq1Nf8sfoKRM6uA4oREzpCX
        elif 'qrcode' in incoming_msg:
            bit_address = incoming_msg.split()[1]
            qr_code_url = f'https://www.bitcoinqrcodemaker.com/api/?style=bitcoin&address={bit_address}'
            msg.body("Here's your Bitcoin QR Code Image!")
            msg.media(qr_code_url)
            responded = True

        # usd check date 2 bitcoins on 12.12.2015
        elif 'check date' in incoming_msg:
            match_date = re.search(r'\d{2}.\d{2}.\d{4}', incoming_msg)
            date = datetime.strptime(match_date.group(), '%d.%m.%Y').date()
            currency = incoming_msg.split()[0].upper()
            symbols = CurrencyCodes()
            bit_amount = float(re.search(r'\d+', incoming_msg).group(0))
            past_date = BtcConverter()
            reply = past_date.convert_btc_to_cur_on(bit_amount, currency, date)
            msg.body(f"{bit_amount} Bitcoins were worth {symbols.get_symbol(currency)}{round(reply, 2)}")
            responded = True

        elif 'get address' in incoming_msg:
            address_request = requests.post('https://api.blockcypher.com/v1/btc/test3/addrs')
            address = address_request.json()
            msg.body(f"Bitcoin address: {str(address['address'])} \n"
                     f"\n"
                     f"Private key: {str(address['private'])} \n"
                     f"\n"
                     f"Public key: {str(address['public'])} \n"
                     f"\n"
                     f"WIF: {str(address['wif'])} \n")
            responded = True

        # latest 1 bitcoin to zar
        elif 'latest' in incoming_msg:
            currency = incoming_msg.split()[4].upper()
            amount = float(re.search(r'\d+', incoming_msg).group(0))
            symbols = CurrencyCodes()
            latest_price = BtcConverter()
            reply = latest_price.convert_btc_to_cur(amount, currency)
            msg.body(f"The latest price of B{amount} to {currency} is {symbols.get_symbol(currency)}{round(reply, 2)}")
            responded = True

        elif incoming_msg == 'news':
            r = requests.get('https://newsapi.org/v2/everything?q=bitcoin&apiKey=3ff5909978da49b68997fd2a1e21fae8')

            if r.status_code == 200:
                data = r.json()
                articles = data['articles'][:5]
                result = ''

                for article in articles:
                    title = article['title']
                    url = article['url']
                    if 'Z' in article['publishedAt']:
                        published_at = datetime.datetime.strptime(article['publishedAt'][:19], "%Y-%m-%dT%H:%M:%S")
                    else:
                        published_at = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%S%z")
                    result += """
*{}*
Read more: {}
_Published at {:02}/{:02}/{:02} {:02}:{:02}:{:02} UTC_
""".format(
                        title,
                        url,
                        published_at.day,
                        published_at.month,
                        published_at.year,
                        published_at.hour,
                        published_at.minute,
                        published_at.second
                    )

            else:
                result = 'I cannot fetch news at this time. Sorry!'

            msg.body(result)
            responded = True

        if not responded:
            msg.body("Please send 'hi' for a menu")

        return HttpResponse(str(resp))
