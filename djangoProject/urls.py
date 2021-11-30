
from django.contrib import admin
from django.urls import path
from core import views
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'categories', views.CategoryModelViewSet, basename="category")
router.register(r'sentiment', views.SentimentModelViewSet, basename="sentiment")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('currencies/', views.CurrencyListAPIView.as_view(), name="currencies")
] + router.urls
