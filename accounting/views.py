from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from itertools import chain
from rest_framework import viewsets, filters, status, pagination, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import pagination
from shop.models import Shop, ShopProducts #Product, Category , ProductAttr, ProductImgs, Attributes, ProductColor, Unit
from cart import models
from cart.models import PostWay, Address, Cart, Order
from cart.serializers import CartSerializer, AddressSerializer, OrderSerializer, PostWaySerializer











#----------------------------------------------------- Exchanges ---------------
class Exchanges(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response('data', status=status.HTTP_200_OK)








#----------------------------------------------------- Sales ---------------
class Sales(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response('data', status=status.HTTP_200_OK)






#----------------------------------------------------- SalesItem ---------------
class SalesItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response('data', status=status.HTTP_200_OK)






#----------------------------------------------------- purchases ---------------
class purchases(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response('data', status=status.HTTP_200_OK)









#----------------------------------------------------- purchases ---------------
class PurchasesItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response('data', status=status.HTTP_200_OK)


#End
