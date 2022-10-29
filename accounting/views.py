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
from partners.models import ExchangePartner
from notice.models import PartnerExchangeNotice










#----------------------------------------------------- Exchanges ---------------
class Exchanges(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        usershops = Shop.objects.filter(user=request.user)
        query = ExchangePartner.objects.filter( Q(user_shop__in=usershops) | Q(partner_shop__in=usershops) )

        shop_ids = []
        for partner in query:
            if partner.user_shop not in usershops:
                shop_ids.append(partner.user_shop.id)
            if partner.partner_shop not in usershops:
                shop_ids.append(partner.partner_shop.id)
        shop_ids = list(set(shop_ids))
        partner_shops = Shop.objects.filter(id__in=shop_ids)

        #partner_exchanges = PartnerExchangeNotice.objects.filter(exchange_partner__user_shop__in=partner_shops, type='buyer_response', answer_status='accepted') # in exchange_partner__user_shop__in should add partner shop too
        response_data=[]
        for item in partner_shops:
            item_data = { 'shop_id':item.id,
                          'shop_name':item.name,
                          'shop_user':item.user.mobile,
                          'shop_user_fname':item.user.first_name,
                          'shop_user_lname':item.user.last_name,
                          'status':'بستانکار',
                          'amount':30000
                        }
            response_data.append(item_data)

        return Response(response_data, status=status.HTTP_200_OK)







#----------------------------------------------------- ExchangesItem ---------------
class ExchangesItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response('data', status=status.HTTP_200_OK)





#----------------------------------------------------- Sales ---------------
class Sales(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        usershops = Shop.objects.filter(user=request.user)
        orders = list(set(Order.objects.filter(carts__product__shop__in=usershops).values_list('code', flat=True)))
        orders = Order.objects.filter(code__in=orders)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        '''
        sales_list=[]
        for obj in query:
            sale = { 'id':obj.id, 'code':obj.code, 'delivery_date':obj.delivery_date, 'delivery_time':obj.delivery_time, 'pay_way':obj.pay_way,
                     'total':obj.total, 'amount':obj.amount, 'status':obj.status, 'admin_note':obj.admin_note,
                     'create_at':obj.create_at, 'update_at':obj.update_at, 'address':obj.address.id, 'post_way':obj.post_way.id, 'cart':'' }
            sales_list.append(sale)
        '''









#----------------------------------------------------- SalesItem ---------------
class SalesItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response('data', status=status.HTTP_200_OK)










#----------------------------------------------------- purchases ---------------
class Purchases(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        order = Order.objects.filter(user=request.user)
        final_data=[]
        for order_item in order:
            shop=[]
            for cart_item in order_item.carts.all():
                shop.append(cart_item.product.shop.id)
            shops=list(set(shop))
            #print(shops)

            ##########
            for cart_item in order_item.carts.all():
                shop_cart_items=[]
                for S in shops:
                    if cart_item.product.shop.id == S:
                        shop_cart_items.append(cart_item.id)

                shopcart={'shop':cart_item.product.shop.id, 'item':shop_cart_items}
             #################

            order_data={'order':order_item.code, 'shops':shopcart}
            final_data.append(order_data)
        return Response(final_data, status=status.HTTP_200_OK)



        '''
        purchase_list=[]
        for obj in query:



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


            purchase = { 'id':obj.id, 'code':obj.code, 'delivery_date':obj.delivery_date, 'delivery_time':obj.delivery_time, 'pay_way':obj.pay_way,
                         'total':obj.total, 'amount':obj.amount, 'status':obj.status, 'admin_note':obj.admin_note,
                         'create_at':obj.create_at, 'update_at':obj.update_at, 'address':obj.address.id, 'post_way':obj.post_way.id, 'cart':'' }
        purchase_list.append(purchase)
        return Response(purchase_list, status=status.HTTP_200_OK)
        '''









#----------------------------------------------------- PurchasesItem ---------------
class PurchasesItem(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        query = get_object_or_404(Order, id=self.kwargs["id"])
        serializer = OrderSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        request.data['user']=request.user.id
        query = get_object_or_404(Order, id=self.kwargs["id"])
        serializer = OrderSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)










#End
