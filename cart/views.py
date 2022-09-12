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
from . import models
from .models import PostWay, Address, Cart, Order
from .serializers import CartSerializer, AddressSerializer, OrderSerializer, PostWaySerializer











#--------------------------------------------- AddressSerializer ---------------
class PostWay(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        query = models.PostWay.objects.all()
        serializer = PostWaySerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)










#--------------------------------------------- AddressSerializer ---------------
class Address(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        query = models.Address.objects.filter(user=request.user)
        serializer = AddressSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        request.data['user'] = request.user.id
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)













#---------------------------------------------------------- Cart ---------------
class AddToCart(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        query = Cart.objects.filter(user=request.user, status='cart')
        serializer = CartSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        request.data['user'] = request.user.id
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








#----------------------------------------------------- Cart Item ---------------
class AddToCartItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = get_object_or_404(Cart, id=self.kwargs["id"])
        serializer = CartSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        query = get_object_or_404(Cart, id=self.kwargs["id"])
        query.delete()
        return Response(status=status.HTTP_200_OK)













#---------------------------------------------------------- Order --------------
class Order(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        query = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        carts = Cart.objects.filter(user=request.user, status='cart')

        request.data['user'] = request.user.id
        request.data['amount'] = carts.count()

        cartlist = []
        for c in carts:
            cartlist.append(c.id)
        request.data['carts'] = cartlist

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








#End
