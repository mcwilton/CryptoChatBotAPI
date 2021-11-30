from django.contrib import admin
from core.models import Currency, Transaction, Category, SentimentData

admin.site.register(Currency)
admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(SentimentData)
