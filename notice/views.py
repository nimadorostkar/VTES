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
from .models import PartnerExchangeNotice
from .serializers import PartnerExchangeNoticeSerializer
import json
from ticket.models import Ticket
from ticket.serializers import TicketSerializer



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
                shop_product = partnering.shop_product.id
            else:
                shop_product = None

            obj = { 'id':partnering.id, 'status':partnering.status, 'type':partnering.type, 'quantity':partnering.quantity,
                    'offer_price':partnering.offer_price, 'date_contract':str(partnering.date_contract), 'accountingId':partnering.accountingId,
                    'description':partnering.description, 'deposit_slip_image':deposit_slip_image, 'shop_product':shop_product,
                    'exchange_partner_id':partnering.exchange_partner.id, 'partner_shop':partner_shop, 'partnerShopName':partnerShopName,
                    'partner_first_name':partner_first_name, 'partner_last_name':partner_last_name, 'partnerShopUser':partnerShopUser,
                    'partnerShopPhone':partnerShopPhone, 'exchange_partner_status':partnering.exchange_partner.status }
            data.append(obj)
        return Response(data, status=status.HTTP_200_OK)





#---------------------------------- ProductExchangeReq in partners -------------
class ProductExchangeReq(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data=request.data
        data['status'] = "unanswered"
        data['type'] = "exchange-request"

        user_shop = Shop.objects.filter(user=request.user).first().id
        partner_shop = ShopProducts.objects.get(id=data['shop_product']).shop.id
        data['exchange_partner'] = ExchangePartner.objects.get( Q(user_shop=user_shop, partner_shop=partner_shop ) | Q( user_shop=partner_shop, partner_shop=user_shop) ).id

        serializer = PartnerExchangeNoticeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        '''
        try:
            notice = PartnerExchangeNotice()
            notice.status = 'unanswered'
            notice.type = 'exchange-request'
            notice.exchange_partner = data['exchange_partner']
            notice.save()
        except:
            return Response('درخواست همکاری ایجاد شد اما مشکلی در ایجاد اعلان به وجود آمده', status=status.HTTP_400_BAD_REQUEST)
        '''



































#--------------------------------------------------- PartnerNotice -------------
class PartnerReq(GenericAPIView):
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
                shop_product = partnering.shop_product.id
            else:
                shop_product = None

            obj = { 'id':partnering.id, 'status':partnering.status, 'type':partnering.type, 'quantity':partnering.quantity,
                    'offer_price':partnering.offer_price, 'date_contract':str(partnering.date_contract), 'accountingId':partnering.accountingId,
                    'description':partnering.description, 'deposit_slip_image':deposit_slip_image, 'shop_product':shop_product,
                    'exchange_partner_id':partnering.exchange_partner.id, 'partner_shop':partner_shop, 'partnerShopName':partnerShopName,
                    'partner_first_name':partner_first_name, 'partner_last_name':partner_last_name, 'partnerShopUser':partnerShopUser,
                    'partnerShopPhone':partnerShopPhone, 'exchange_partner_status':partnering.exchange_partner.status }
            data.append(obj)
        return Response(data, status=status.HTTP_200_OK)










class PartnerReqItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
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
                'description':partnering.description, 'deposit_slip_image':deposit_slip_image, 'shop_product':partnering.shop_product,
                'exchange_partner_id':partnering.exchange_partner.id, 'partner_shop':partner_shop, 'partnerShopName':partnerShopName,
                'partner_first_name':partner_first_name, 'partner_last_name':partner_last_name, 'partnerShopUser':partnerShopUser,
                'partnerShopPhone':partnerShopPhone, 'exchange_partner_status':partnering.exchange_partner.status }
        return Response(data, status=status.HTTP_200_OK)



    def put(self, request, *args, **kwargs):
        pe = get_object_or_404(PartnerExchangeNotice, id=self.kwargs["id"])
        request.data['user_shop'] = pe.exchange_partner.user_shop.id
        request.data['partner_shop'] = pe.exchange_partner.partner_shop.id
        exchange = get_object_or_404(ExchangePartner, id=pe.exchange_partner.id )
        exchange_serializer = ExchangePartnerSerializer(exchange, data=request.data)
        if exchange_serializer.is_valid():
            exchange_serializer.save()
            if request.data['status'] == 'تایید شده':
                notice = PartnerExchangeNotice()
                notice.exchange_partner = exchange
                notice.status = 'unanswerable'
                notice.type = 'cooperation-request-answer'
                notice.save()
            elif request.data['status'] == 'رد شده':
                notice = PartnerExchangeNotice()
                notice.exchange_partner = exchange
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

        data = { 'id':partnering.id, 'status':partnering.status, 'type':partnering.type, 'quantity':partnering.quantity,
                'offer_price':partnering.offer_price, 'date_contract':partnering.date_contract, 'accountingId':partnering.accountingId,
                'description':partnering.description, 'deposit_slip_image':deposit_slip_image, 'shop_product':partnering.shop_product,
                'exchange_partner_id':partnering.exchange_partner.id, 'partner_shop':partner_shop, 'partnerShopName':partnerShopName,
                'partner_first_name':partner_first_name, 'partner_last_name':partner_last_name, 'partnerShopUser':partnerShopUser,
                'partnerShopPhone':partnerShopPhone, 'exchange_partner_status':partnering.exchange_partner.status }
        return Response(data, status=status.HTTP_200_OK)








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













#----------------------------------------------------- ExchangeReq -------------
class ExchangeReq(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExchangePartnerSerializer
    pagination_class = CustomPagination
    queryset = PartnerExchangeNotice.objects.all()
    #filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    #filterset_fields = ['partner_shop', 'status', 'partner_shop__name', 'partner_shop__province', 'partner_shop__city', 'partner_shop__user', 'partner_shop__phone']
    #search_fields = ['user_shop__name', 'partner_shop__name', 'status', 'partner_shop__user__first_name', 'partner_shop__user__last_name']
    #ordering_fields = ['id', 'partner_shop', 'status', 'partner_shop__name', 'partner_shop__address', 'partner_shop__user__first_name', 'partner_shop__user__last_name', 'partner_shop__user', 'partner_shop__phone']


    def get(self, request, format=None):
        usershops = Shop.objects.filter(user=request.user)
        query = self.filter_queryset(PartnerExchangeNotice.objects.filter( Q(user_shop__in=usershops) | Q(partner_shop__in=usershops) and Q(type=usershops) ) )



        shop_ids = []
        for partner in query:
            if partner.user_shop not in usershops:
                shop_ids.append(partner.user_shop.id)
            if partner.partner_shop not in usershops:
                shop_ids.append(partner.partner_shop.id)
        shop_ids = list(set(shop_ids))
        partner_shops = Shop.objects.filter(id__in=shop_ids)

        data = []
        for P in partner_shops:
            exPartner = ExchangePartner.objects.get( Q( user_shop__in=usershops, partner_shop=P ) | Q( user_shop=P, partner_shop__in=usershops) )
            partner_data = { 'shop_id':P.id, 'shop_slug':P.slug, 'shop_name':P.name, 'shop_user':P.user.id, 'owner_name':P.user.first_name +' '+P.user.last_name,
                             'shop_phone':P.phone, 'shop_address':P.address, 'partnership_id':exPartner.id, 'status':exPartner.status }
            data.append(partner_data)

        page = self.paginate_queryset(data)
        if page is not None:
            return self.get_paginated_response(data)
        return Response(data, status=status.HTTP_200_OK)




    def post(self, request, format=None):
        data=request.data
        data['user_shop'] = Shop.objects.filter(user=request.user).first().id
        data['status'] = "در انتظار تایید"

        if data['partner_shop'] == data['user_shop']:
            return Response('نمی‌توانید فروشگاه خود را به لیست همکاری اضافه کنید', status=status.HTTP_400_BAD_REQUEST)

        partnerExist = ExchangePartner.objects.filter( Q( user_shop=data['user_shop'], partner_shop=data['partner_shop'] ) | Q( user_shop=data['partner_shop'], partner_shop=data['user_shop']) )
        if partnerExist:
            return Response('فروشگاه مورد نظر در لیست همکاران شما موجود میباشد و یا درخواست همکاری پیش از این ارسال شده است', status=status.HTTP_400_BAD_REQUEST)

        serializer = ExchangePartnerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            try:
                notice = PartnerExchangeNotice()
                notice.status = 'unanswered'
                notice.type = 'cooperation-request'
                notice.exchange_partner = ExchangePartner.objects.get(id=serializer.data['id'])
                notice.save()
            except:
                return Response('درخواست همکاری ایجاد شد اما مشکلی در ایجاد اعلان به وجود آمده', status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









#----------------------------------------------------- PartnerItem -------------
class ExchangeReqItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        partner = ExchangePartner.objects.get(id=self.kwargs["id"])
        serializer = ExchangePartnerSerializer(partner)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        partner = ExchangePartner.objects.get(id=self.kwargs["id"])
        data=request.data
        data['user_shop']=partner.user_shop.id
        data['partner_shop']=partner.partner_shop.id
        serializer = ExchangePartnerSerializer(partner, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        partner = ExchangePartner.objects.get(id=self.kwargs["id"])
        partner.delete()
        return Response(status=status.HTTP_200_OK)













#end
