import requests
from .models import SentimentData


def my_scheduled_job():
    job_response = requests.get('https://api.senticrypt.com/v1/bitcoin.json')
    scheduled_data = job_response.json()
    # print(data)
    sentiment = scheduled_data[-1]

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

