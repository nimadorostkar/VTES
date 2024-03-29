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
from partners.models import ExchangePartner
from partners.serializers import ExchangePartnerSerializer
from shop.models import Shop, ShopProducts #Product, Category , ProductAttr, ProductImgs, Attributes, ProductColor, Unit
from .models import PartnerExchangeNotice, ReturnedMoney
from .serializers import PartnerExchangeNoticeSerializer
import json
from ticket.models import Ticket
from ticket.serializers import TicketSerializer
from cart.models import Order, Cart, DetermineAvailability


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100








#--------------------------------------------------- PartnerNotice -------------
class PartnerNotice(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PartnerExchangeNoticeSerializer
    pagination_class = CustomPagination
    queryset = PartnerExchangeNotice.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'type', 'accountingId', 'exchange_partner', 'exchange_partner__user_shop', 'exchange_partner__partner_shop', 'exchange_partner__status']
    search_fields = ['exchange_partner__user_shop__name', 'exchange_partner__partner_shop__name', 'exchange_partner__status', 'exchange_partner__partner_shop__user__first_name', 'exchange_partner__partner_shop__user__last_name']
    ordering_fields = ['id', 'date_contract']


    def get(self, request, format=None):
        usershops = Shop.objects.filter(user=request.user)
        query = self.filter_queryset(PartnerExchangeNotice.objects.filter( Q(exchange_partner__partner_shop__in=usershops) | Q(exchange_partner__user_shop__in=usershops) ))

        data = []
        for partnering in query:

            if partnering.type == 'cooperation-request-answer' and partnering.exchange_partner.user_shop not in usershops:
                continue
            if partnering.type == 'cooperation-request' and partnering.exchange_partner.user_shop in usershops:
                continue
            if partnering.type == 'exchange-request' and partnering.shop_product.shop not in usershops:
                continue
            if partnering.type == 'exchange-request-answer' and partnering.shop_product.shop in usershops:
                continue
            if partnering.type == 'buyer_response' and partnering.shop_product.shop in usershops:
                continue

            if partnering.deposit_slip_image:
                deposit_slip_image = partnering.deposit_slip_image.url
            else:
                deposit_slip_image = None

            if partnering.exchange_partner.user_shop in usershops:
                partner_shop = partnering.exchange_partner.partner_shop.id
                partnerShopName = partnering.exchange_partner.partner_shop.name
                partner_first_name = partnering.exchange_partner.partner_shop.user.first_name
                partner_last_name = partnering.exchange_partner.partner_shop.user.last_name
                partnerShopUser = partnering.exchange_partner.partner_shop.user.mobile
                partnerShopPhone = partnering.exchange_partner.partner_shop.phone
            else:
                partner_shop = partnering.exchange_partner.user_shop.id
                partnerShopName = partnering.exchange_partner.user_shop.name
                partner_first_name = partnering.exchange_partner.user_shop.user.first_name
                partner_last_name = partnering.exchange_partner.user_shop.user.last_name
                partnerShopUser = partnering.exchange_partner.user_shop.user.mobile
                partnerShopPhone = partnering.exchange_partner.user_shop.phone

            if partnering.shop_product:
                shop_product = {'shop_product_id':partnering.shop_product.id, 'name':partnering.shop_product.product.name,
                                'brand_id':partnering.shop_product.product.brand.id, 'brand_fname':partnering.shop_product.product.brand.fname,
                                'brand_name':partnering.shop_product.product.brand.name, 'unit_measurment':partnering.shop_product.unit.name }
            else:
                shop_product = None

            obj = { 'id':partnering.id, 'answer_status':partnering.answer_status, 'status':partnering.status, 'type':partnering.type, 'quantity':partnering.quantity,
                    'offer_price':partnering.offer_price, 'date_contract':str(partnering.date_contract), 'accountingId':partnering.accountingId,
                    'description':partnering.description, 'deposit_slip_image':deposit_slip_image, 'shop_product':shop_product,
                    'exchange_partner_id':partnering.exchange_partner.id, 'partner_shop':partner_shop, 'partnerShopName':partnerShopName,
                    'partner_first_name':partner_first_name, 'partner_last_name':partner_last_name, 'partnerShopUser':partnerShopUser,
                    'partnerShopPhone':partnerShopPhone, 'exchange_partner_status':partnering.exchange_partner.status }
            data.append(obj)
        return Response(data, status=status.HTTP_200_OK)









#----------------------------------------------- PartnerNoticeItem -------------
class PartnerNoticeItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = PartnerExchangeNoticeSerializer

    def get(self, request, *args, **kwargs):
        usershops = Shop.objects.filter(user=request.user)
        partnering = get_object_or_404(PartnerExchangeNotice, id=self.kwargs["id"])

        if partnering.deposit_slip_image:
            deposit_slip_image = partnering.deposit_slip_image.url
        else:
            deposit_slip_image = None

        if partnering.exchange_partner.user_shop in usershops:
            partner_shop = partnering.exchange_partner.partner_shop.id
            partnerShopName = partnering.exchange_partner.partner_shop.name
            partner_first_name = partnering.exchange_partner.partner_shop.user.first_name
            partner_last_name = partnering.exchange_partner.partner_shop.user.last_name
            partnerShopUser = partnering.exchange_partner.partner_shop.user.mobile
            partnerShopPhone = partnering.exchange_partner.partner_shop.phone
        else:
            partner_shop = partnering.exchange_partner.user_shop.id
            partnerShopName = partnering.exchange_partner.user_shop.name
            partner_first_name = partnering.exchange_partner.user_shop.user.first_name
            partner_last_name = partnering.exchange_partner.user_shop.user.last_name
            partnerShopUser = partnering.exchange_partner.user_shop.user.mobile
            partnerShopPhone = partnering.exchange_partner.user_shop.phone

        data = { 'id':partnering.id, 'status':partnering.status, 'type':partnering.type, 'quantity':partnering.quantity,
                'offer_price':partnering.offer_price, 'date_contract':partnering.date_contract, 'accountingId':partnering.accountingId,
                'description':partnering.description, 'deposit_slip_image':deposit_slip_image, 'shop_product':partnering.shop_product.id,
                'exchange_partner_id':partnering.exchange_partner.id, 'partner_shop':partner_shop, 'partnerShopName':partnerShopName,
                'partner_first_name':partner_first_name, 'partner_last_name':partner_last_name, 'partnerShopUser':partnerShopUser,
                'partnerShopPhone':partnerShopPhone, 'exchange_partner_status':partnering.exchange_partner.status }
        return Response(data, status=status.HTTP_200_OK)



    def put(self, request, *args, **kwargs):
        pe = get_object_or_404(PartnerExchangeNotice, id=self.kwargs["id"])
        request.data['answer_status'] = 'accepted'
        request.data['user_shop'] = pe.exchange_partner.user_shop.id
        request.data['partner_shop'] = pe.exchange_partner.partner_shop.id
        exchange = get_object_or_404(ExchangePartner, id=pe.exchange_partner.id )
        exchange_serializer = ExchangePartnerSerializer(exchange, data=request.data)
        if exchange_serializer.is_valid():
            exchange_serializer.save()
            if request.data['status'] == 'تایید شده':
                notice = PartnerExchangeNotice()
                notice.exchange_partner = exchange
                notice.answer_status = 'accepted'
                notice.status = 'unanswerable'
                notice.type = 'cooperation-request-answer'
                notice.save()
            elif request.data['status'] == 'رد شده':
                notice = PartnerExchangeNotice()
                notice.exchange_partner = exchange
                notice.answer_status = 'declined'
                notice.status = 'unanswerable'
                notice.type = 'cooperation-request-answer'
                notice.save()
        else:
            return Response(exchange_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        request.data['status'] = request.data['notice_status']
        partner_exchange = get_object_or_404(PartnerExchangeNotice, id=self.kwargs["id"])
        serializer = PartnerExchangeNoticeSerializer(partner_exchange, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        usershops = Shop.objects.filter(user=request.user)
        partnering = partner_exchange

        if partnering.deposit_slip_image:
            deposit_slip_image = partnering.deposit_slip_image.url
        else:
            deposit_slip_image = None

        if partnering.exchange_partner.user_shop in usershops:
            partner_shop = partnering.exchange_partner.partner_shop.id
            partnerShopName = partnering.exchange_partner.partner_shop.name
            partner_first_name = partnering.exchange_partner.partner_shop.user.first_name
            partner_last_name = partnering.exchange_partner.partner_shop.user.last_name
            partnerShopUser = partnering.exchange_partner.partner_shop.user.mobile
            partnerShopPhone = partnering.exchange_partner.partner_shop.phone
        else:
            partner_shop = partnering.exchange_partner.user_shop.id
            partnerShopName = partnering.exchange_partner.user_shop.name
            partner_first_name = partnering.exchange_partner.user_shop.user.first_name
            partner_last_name = partnering.exchange_partner.user_shop.user.last_name
            partnerShopUser = partnering.exchange_partner.user_shop.user.mobile
            partnerShopPhone = partnering.exchange_partner.user_shop.phone

        data = { 'id':partnering.id, 'answer_status':partnering.answer_status, 'status':partnering.status, 'type':partnering.type, 'quantity':partnering.quantity,
                'offer_price':partnering.offer_price, 'date_contract':partnering.date_contract, 'accountingId':partnering.accountingId,
                'description':partnering.description, 'deposit_slip_image':deposit_slip_image, 'shop_product':partnering.shop_product,
                'exchange_partner_id':partnering.exchange_partner.id, 'partner_shop':partner_shop, 'partnerShopName':partnerShopName,
                'partner_first_name':partner_first_name, 'partner_last_name':partner_last_name, 'partnerShopUser':partnerShopUser,
                'partnerShopPhone':partnerShopPhone, 'exchange_partner_status':partnering.exchange_partner.status }
        return Response(data, status=status.HTTP_200_OK)



    def post(self, request, *args, **kwargs):
        pe = get_object_or_404(PartnerExchangeNotice, id=self.kwargs["id"])

        if request.data['answer_status'] == 'accepted':
            ans_notice = PartnerExchangeNotice()
            ans_notice.exchange_partner = pe.exchange_partner
            ans_notice.shop_product = pe.shop_product
            ans_notice.quantity = pe.quantity
            ans_notice.status = 'unanswerable'
            ans_notice.type = 'exchange-request-answer'
            ans_notice.offer_price = pe.offer_price
            ans_notice.date_contract = pe.date_contract
            ans_notice.answer_status = 'accepted'
            ans_notice.description = request.data['description']
            ans_notice.save()
            serializer = PartnerExchangeNoticeSerializer(ans_notice)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.data['answer_status'] == 'declined':
            ans_notice = PartnerExchangeNotice()
            ans_notice.exchange_partner = pe.exchange_partner
            ans_notice.shop_product = pe.shop_product
            ans_notice.quantity = pe.quantity
            ans_notice.status = 'unanswerable'
            ans_notice.type = 'exchange-request-answer'
            ans_notice.offer_price = pe.offer_price
            ans_notice.date_contract = pe.date_contract
            ans_notice.answer_status = 'declined'
            ans_notice.description = request.data['description']
            ans_notice.save()
            serializer = PartnerExchangeNoticeSerializer(ans_notice)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.data['answer_status'] == 'changed-value':
            ans_notice = PartnerExchangeNotice()
            ans_notice.exchange_partner = pe.exchange_partner
            ans_notice.shop_product = pe.shop_product
            ans_notice.quantity = pe.quantity
            ans_notice.status = 'answered'
            ans_notice.type = 'exchange-request-answer'
            ans_notice.offer_price = request.data['offer_price']
            ans_notice.quantity = request.data['quantity']
            ans_notice.date_contract = request.data['date_contract']
            ans_notice.description = request.data['description']
            ans_notice.answer_status = 'changed-value'
            ans_notice.save()
            serializer = PartnerExchangeNoticeSerializer(ans_notice)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response('specify the answer status', status=status.HTTP_400_BAD_REQUEST)






#---------------------------------- ProductExchangeReq in partners -------------
class ProductExchangeReq(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data=request.data

        try:
            user_shop = Shop.objects.filter(user=request.user).first().id
            partner_shop = ShopProducts.objects.get(id=data['shop_product']).shop.id
            exchange = PartnerExchangeNotice()
            exchange.status = "unanswered"
            exchange.type = "exchange-request"
            exchange.exchange_partner = ExchangePartner.objects.get( Q(user_shop=user_shop, partner_shop=partner_shop ) | Q( user_shop=partner_shop, partner_shop=user_shop) )
            exchange.shop_product = ShopProducts.objects.get(id=data['shop_product'])
            exchange.quantity = data['quantity']
            exchange.offer_price = data['offer_price']
            exchange.date_contract = data['date_contract']
            exchange.description = data['description']
            exchange.save()
            serializer = PartnerExchangeNoticeSerializer(exchange)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response('partner shop not found', status=status.HTTP_400_BAD_REQUEST)





#--------------------------------------------------- PartnerNotice -------------
class TicketNotice(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    pagination_class = CustomPagination
    queryset = Ticket.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'answer_status', 'type', 'state', 'user', 'title']
    search_fields = ['title', 'user__first_name', 'user__last_name', 'description', 'admin_ans']
    ordering_fields = ['id', 'created_date', 'status']

    def get(self, request, format=None):
        query = self.filter_queryset(Ticket.objects.filter(user=request.user))
        page = self.paginate_queryset(query)
        if page is not None:
            serializer = TicketSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TicketSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)








#----------------------------------------------------- SalesOrders -------------
class SalesOrders(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        usershops = Shop.objects.filter(user=request.user)
        query = Order.objects.filter(user=request.user)
        orders=[]
        for obj in query:
            items=[]
            for cart in obj.carts.all():
                if cart.product.shop in usershops:
                    if cart.quantity >= 1:
                        price = cart.product.one_price
                    elif cart.quantity >= cart.product.medium_volume_qty:
                        price = cart.product.medium_volume_price
                    elif cart.quantity >= cart.product.wholesale_volume_qty:
                        price = cart.product.wholesale_volume_price
                    else:
                        price = '-'

                    item = {'cart_id':cart.id, 'product_id':cart.product.id, 'product':cart.product.product.name, 'price':price, 'quantity':cart.quantity, 'unit':cart.product.unit.name, 'brand':cart.product.product.brand.name, 'brand_f':cart.product.product.brand.fname, 'product_img':cart.product.product.banner.url}
                    items.append(item)
            order = {'orders_code':obj.code, 'orders_status':obj.status, 'items':items}
            orders.append(order)
        return Response(orders, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        data=request.data
        order_code=data['order_code']
        carts=data['carts']

        carts_ids=[]
        for c in carts:
            carts_ids.append(c['cart_id'])
        order_carts = list(Order.objects.filter(code=order_code).values_list('carts', flat=True))
        not_found_carts=[]
        for item in order_carts:
            if item not in carts_ids:
                not_found_carts.append(item)

        if not_found_carts:
            return Response('In this order, you must also specify this items: {}'.format(not_found_carts), status=status.HTTP_400_BAD_REQUEST)

        for cart in carts:
            try:
                DA = DetermineAvailability()
                DA.order = Order.objects.get(code=order_code)
                DA.cart = Cart.objects.get(id=cart['cart_id'])
                DA.status = cart['status']
                DA.save()
            except:
                return Response('Cart Id not found ({})'.format(cart['cart_id']), status=status.HTTP_400_BAD_REQUEST)

        order=Order.objects.get(code=order_code)
        order.status='Accepted'
        order.save()

        return Response(status=status.HTTP_200_OK)






#--------------------------------------------------- PurchaseOrders ------------
class PurchaseOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        DA = DetermineAvailability.objects.all()
        query = Order.objects.filter(user=request.user)
        returned_money=0
        orders=[]
        for obj in query:
            items=[]
            s='در انتظار تایید فروشگاه'
            for cart in obj.carts.all():
                for da in DA:
                    if obj == da.order and cart==da.cart:
                        s=da.status

                if cart.quantity >= 1:
                    price = cart.product.one_price
                elif cart.quantity >= cart.product.medium_volume_qty:
                    price = cart.product.medium_volume_price
                elif cart.quantity >= cart.product.wholesale_volume_qty:
                    price = cart.product.wholesale_volume_price
                else:
                    price = 0

                if s=="not-confirmed":
                    returned_money+=price

                item = {'shop':cart.product.shop.name, 'product':cart.product.product.name, 'unit':cart.product.unit.name, 'brand':cart.product.product.brand.name, 'brand_f':cart.product.product.brand.fname, 'quantity':cart.quantity, 'price':price, 'status':s, 'product_img':cart.product.product.banner.url }
                items.append(item)

            re_money, created = ReturnedMoney.objects.update_or_create(order=obj)
            re_money.amount=returned_money
            re_money.save()

            order = {'order_code':obj.code, 'orders_status':obj.status, 'items':items}
            orders.append(order)

            response = {'orders':orders, 'returned_money':returned_money}
        return Response(response, status=status.HTTP_200_OK)







#----------------------------------------------------------- Count ------------
class Count(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        usershops = Shop.objects.filter(user=request.user)
        query = PartnerExchangeNotice.objects.filter( Q(exchange_partner__partner_shop__in=usershops) | Q(exchange_partner__user_shop__in=usershops) )
        tickets = Ticket.objects.filter(user=request.user)
        purchase_orders = Order.objects.filter(carts__product__shop__in=usershops)

        data = {
                'all_notices':query.count(),
                'unanswered_notices':query.filter(status='unanswered').count(),
                'tickets':tickets.count(),
                'new_tickets':tickets.filter(status='New').count(),
                'answered_new_tickets':tickets.filter(status='Accepted', state=True).count(),
                'purchase_orders': purchase_orders.count(),
                'unconfirmed_purchase_orders': purchase_orders.filter(status="New").count(),
                'sale_orders':Order.objects.filter(user=request.user).count(),
                'new_sale_orders':Order.objects.filter(user=request.user, status='New').count(),
                'answered_status':query.filter(status='answered').count(),
                'unanswered_status':query.filter(status='unanswered').count(),
                'unanswerable_status':query.filter(status='unanswerable').count(),
                'accepted_answer_status':query.filter(answer_status='accepted').count(),
                'declined_answer_status':query.filter(answer_status='declined').count(),
                'changed_value_answer_status':query.filter(answer_status='changed-value').count(),
                'cooperation_req_type':query.filter(type='cooperation-request').count(),
                'cooperation_req_answer_type':query.filter(type='cooperation-request-answer').count(),
                'exchange_req_answer_type':query.filter(type='exchange-request-answer').count(),
                'buyer_response_type':query.filter(type='buyer_response').count(),
                'debtor_reposnse_accounting_type':query.filter(type='debtor-reposnse-accounting').count(),
                'creditor_alert_accounting_type':query.filter(type='creditor-alert-accounting').count(),
                'creditor_answer_accounting_type':query.filter(type='creditor-answer-accounting').count()
               }
        return Response(data, status=status.HTTP_200_OK)








#end
