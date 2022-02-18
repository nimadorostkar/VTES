from django.shortcuts import render
from .serializers import ShopSerializer
from rest_framework import viewsets
from .models import Shop, Product, Product_Attr, Category , Attributes








class ShopView(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
