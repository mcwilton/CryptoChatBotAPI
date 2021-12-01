
from django.contrib import admin
from django.urls import path, include
from core import views
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'categories_api', views.CategoryModelViewSet, basename="category")
router.register(r'sentiment_api', views.SentimentModelViewSet, basename="sentiment")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('currencies/', views.CurrencyListAPIView.as_view(), name="currencies"),
    path('', include('core.urls')),
] + router.urls
