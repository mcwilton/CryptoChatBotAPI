from rest_framework.generics import ListAPIView
from core.serializers import CurrencySerializer, CategorySerializer
from core.models import Currency, Category
from rest_framework.viewsets import ModelViewSet


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
