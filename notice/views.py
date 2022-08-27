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
from shop.models import Shop #Product, Category , ProductAttr, ProductImgs, ShopProducts, Attributes, ProductColor, Unit
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
            if partnering.deposit_slip_image:
                deposit_slip_image = partnering.deposit_slip_image.url
            else:
                deposit_slip_image = None
            obj = { 'id':partnering.id, 'status':partnering.status, 'type':partnering.type, 'quantity':partnering.quantity,
                    'offer_price':partnering.offer_price, 'date_contract':partnering.date_contract, 'accountingId':partnering.accountingId,
                    'description':partnering.description, 'deposit_slip_image':deposit_slip_image, 'shop_product':partnering.shop_product,
                    'exchange_partner_id':partnering.exchange_partner.id, 'partner_shop':partnering.exchange_partner.user_shop.id, 'partnerShopName':partnering.exchange_partner.user_shop.name,
                    'partner_first_name':partnering.exchange_partner.user_shop.user.first_name, 'partner_last_name':partnering.exchange_partner.user_shop.user.last_name, 'partnerShopUser':partnering.exchange_partner.user_shop.user.mobile,
                    'partnerShopPhone':partnering.exchange_partner.user_shop.phone, 'exchange_partner_status':partnering.exchange_partner.status }
            data.append(obj)
        return Response(data, status=status.HTTP_200_OK)












class PartnerReqItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = PartnerExchangeNoticeSerializer

    def get(self, request, *args, **kwargs):
        partnering = get_object_or_404(PartnerExchangeNotice, id=self.kwargs["id"])
        if partnering.deposit_slip_image:
            deposit_slip_image = partnering.deposit_slip_image.url
        else:
            deposit_slip_image = None
        data = { 'id':partnering.id, 'status':partnering.status, 'type':partnering.type, 'quantity':partnering.quantity,
                'offer_price':partnering.offer_price, 'date_contract':partnering.date_contract, 'accountingId':partnering.accountingId,
                'description':partnering.description, 'deposit_slip_image':deposit_slip_image, 'shop_product':partnering.shop_product,
                'exchange_partner_id':partnering.exchange_partner.id, 'partner_shop':partnering.exchange_partner.user_shop.id, 'partnerShopName':partnering.exchange_partner.user_shop.name,
                'partner_first_name':partnering.exchange_partner.user_shop.user.first_name, 'partner_last_name':partnering.exchange_partner.user_shop.user.last_name, 'partnerShopUser':partnering.exchange_partner.user_shop.user.mobile,
                'partnerShopPhone':partnering.exchange_partner.user_shop.phone, 'exchange_partner_status':partnering.exchange_partner.status }
        print(data)
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
                notice.status = 'answered'
                notice.type = 'cooperation-request-answer'
                notice.save()
            elif request.data['status'] == 'رد شده':
                notice = PartnerExchangeNotice()
                notice.exchange_partner = exchange
                notice.status = 'answered'
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

        return Response(serializer.data, status=status.HTTP_200_OK)









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
















#end
