from django.db import models
import datetime




class SentimentData(models.Model):
    comment = models.CharField(max_length=100, null=True, blank=True)
    rate = models.FloatField()
    count = models.IntegerField(null=True)
    median = models.FloatField()
    mean = models.FloatField()
    polarity = models.FloatField()
    sum = models.FloatField(null=True)
    btc_price = models.FloatField()
    date_time = models.DateTimeField(datetime.datetime.now())

    # def __str__(self):
    #     return self.comment


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="transactions")
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="transactions")

    def __str__(self):
        return f"{self.amount} {self.currency.code} {self.date}"
