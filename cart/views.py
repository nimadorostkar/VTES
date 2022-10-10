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








#----------------------------------------------------- AddressItem -------------
class AddressItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = get_object_or_404(models.Address, id=self.kwargs["id"])
        serializer = AddressSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        request.data['user']=request.user.id
        query = get_object_or_404(models.Address, id=self.kwargs["id"])
        serializer = AddressSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        query = get_object_or_404(models.Address, id=self.kwargs["id"])
        query.delete()
        return Response(status=status.HTTP_200_OK)












#----------------------------------------------------- Cart list ---------------
class Cart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        query = models.Cart.objects.filter(user=request.user, status='cart')
        cart_list = []
        for obj in query:

            if obj.product.unit:
                unit = obj.product.unit.name
            else:
                unit = None

            cart = { 'id':obj.id, 'product_id':obj.product.id, 'quantity':obj.quantity, 'product_name':obj.product.product.name, 'product_approved':obj.product.product.approved,
                     'product_code':obj.product.product.code, 'product_irancode':obj.product.product.irancode, 'product_brand_name':obj.product.product.brand.name, 'product_brand_fname':obj.product.product.brand.fname,
                     'product_link':obj.product.product.link, 'product_description':obj.product.product.description, 'product_banner':obj.product.product.banner.url,
                     'product_internal_code':obj.product.internal_code, 'product_unit':unit, 'product_price_model':obj.product.price_model, 'product_one_price':obj.product.one_price,
                     'product_medium_volume_price':obj.product.medium_volume_price, 'product_medium_volume_qty':obj.product.medium_volume_qty, 'product_wholesale_volume_price':obj.product.wholesale_volume_price, 'product_wholesale_volume_qty':obj.product.wholesale_volume_qty,
                     'product_category_id':obj.product.product.category.id, 'product_category_name':obj.product.product.category.name, 'product_shop':obj.product.shop.name, 'product_shop_id':obj.product.shop.id     }
            cart_list.append(cart)
        return Response(cart_list, status=status.HTTP_200_OK)








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

            obj = models.Cart.objects.get(id=serializer.data['id'])

            if obj.product.unit:
                unit = obj.product.unit.name
            else:
                unit = None

            cart = { 'id':obj.id, 'product_id':obj.product.id, 'quantity':obj.quantity, 'product_name':obj.product.product.name, 'product_approved':obj.product.product.approved,
                     'product_code':obj.product.product.code, 'product_irancode':obj.product.product.irancode, 'product_brand_name':obj.product.product.brand.name, 'product_brand_fname':obj.product.product.brand.fname,
                     'product_link':obj.product.product.link, 'product_description':obj.product.product.description, 'product_banner':obj.product.product.banner.url,
                     'product_internal_code':obj.product.internal_code, 'product_unit':unit, 'product_price_model':obj.product.price_model, 'product_one_price':obj.product.one_price,
                     'product_medium_volume_price':obj.product.medium_volume_price, 'product_medium_volume_qty':obj.product.medium_volume_qty, 'product_wholesale_volume_price':obj.product.wholesale_volume_price, 'product_wholesale_volume_qty':obj.product.wholesale_volume_qty,
                     'product_category_id':obj.product.product.category.id, 'product_category_name':obj.product.product.category.name, 'product_shop':obj.product.shop.name, 'product_shop_id':obj.product.shop.id     }

            return Response(cart, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








#----------------------------------------------------- Cart Item ---------------
class AddToCartItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = get_object_or_404(models.Cart, id=self.kwargs["id"])
        serializer = CartSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        request.data['user']=request.user.id
        query = get_object_or_404(models.Cart, id=self.kwargs["id"])
        serializer = CartSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()

            obj = models.Cart.objects.get(id=serializer.data['id'])

            if obj.product.unit:
                unit = obj.product.unit.name
            else:
                unit = None

            cart = { 'id':obj.id, 'product_id':obj.product.id, 'quantity':obj.quantity, 'product_name':obj.product.product.name, 'product_approved':obj.product.product.approved,
                     'product_code':obj.product.product.code, 'product_irancode':obj.product.product.irancode, 'product_brand_name':obj.product.product.brand.name, 'product_brand_fname':obj.product.product.brand.fname,
                     'product_link':obj.product.product.link, 'product_description':obj.product.product.description, 'product_banner':obj.product.product.banner.url,
                     'product_internal_code':obj.product.internal_code, 'product_unit':unit, 'product_price_model':obj.product.price_model, 'product_one_price':obj.product.one_price,
                     'product_medium_volume_price':obj.product.medium_volume_price, 'product_medium_volume_qty':obj.product.medium_volume_qty, 'product_wholesale_volume_price':obj.product.wholesale_volume_price, 'product_wholesale_volume_qty':obj.product.wholesale_volume_qty,
                     'product_category_id':obj.product.product.category.id, 'product_category_name':obj.product.product.category.name, 'product_shop':obj.product.shop.name, 'product_shop_id':obj.product.shop.id     }

            return Response(cart, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        query = get_object_or_404(models.Cart, id=self.kwargs["id"])
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
        carts = models.Cart.objects.filter(user=request.user, status='cart')

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
