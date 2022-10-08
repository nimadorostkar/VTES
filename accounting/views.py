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
from shop.models import Shop, ShopProducts, Product, Category , ProductAttr, ProductImgs, Attributes, ProductColor, Unit
from cart import models
from cart.models import PostWay, Address, Cart, Order
from cart.serializers import CartSerializer, AddressSerializer, OrderSerializer, PostWaySerializer











#----------------------------------------------------- Exchanges ---------------
class Exchanges(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response('data', status=status.HTTP_200_OK)







#----------------------------------------------------- ExchangesItem ---------------
class ExchangesItem(APIView):
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
class Purchases(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        query = Order.objects.filter(user=request.user)
        purchase_list=[]
        for obj in query:

            '''

            shops=[]
            for cart in obj.carts.all():
                shops.append(cart.product.shop.id)
                products = ShopProducts.objects.filter(id=cart.product.id)
            shops_id = list(set(shops))

            for shop in shops_id:
                for product in products:
                    product_list=[]
                    if product.shop.id == shop.id:
                        item = ShopProducts.objects.get(id=product.id)
                        product_list.append(item)
                aa = {'shop':shop.name, 'products':product_list }
            '''

            purchase = { 'id':obj.id, 'code':obj.code, 'delivery_date':obj.delivery_date, 'delivery_time':obj.delivery_time, 'pay_way':obj.pay_way,
                         'total':obj.total, 'amount':obj.amount, 'status':obj.status, 'admin_note':obj.admin_note,
                         'create_at':obj.create_at, 'update_at':obj.update_at, 'address':obj.address.id, 'post_way':obj.post_way.id, 'cart':'' }
        purchase_list.append(purchase)
        return Response(purchase_list, status=status.HTTP_200_OK)










#----------------------------------------------------- PurchasesItem ---------------
class PurchasesItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response('data', status=status.HTTP_200_OK)








#End
