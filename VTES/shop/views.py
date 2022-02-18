from django.shortcuts import render
from .serializers import ShopSerializer
from rest_framework import viewsets
from .models import Shop, Product, Product_Attr, Category , Attributes








class ShopSerializer(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
