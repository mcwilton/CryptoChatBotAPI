from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'broadcast$', views.broadcast_sms, name="default"),
    url(r'', views.get_sentiment_data, name="index")
]
