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




class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100








#--------------------------------------------------- PartnerNotice -------------
class PartnerNotice(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExchangePartnerSerializer
    pagination_class = CustomPagination
    queryset = ExchangePartner.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['partner_shop', 'status', 'partner_shop__name', 'partner_shop__province', 'partner_shop__city', 'partner_shop__user', 'partner_shop__phone']
    search_fields = ['user_shop__name', 'partner_shop__name', 'status', 'partner_shop__user__first_name', 'partner_shop__user__last_name']
    ordering_fields = ['id', 'partner_shop', 'status', 'partner_shop__name', 'partner_shop__address', 'partner_shop__user__first_name', 'partner_shop__user__last_name', 'partner_shop__user', 'partner_shop__phone']


    def get(self, request, format=None):
        usershops = Shop.objects.filter(user=request.user)
        query = self.filter_queryset(ExchangePartner.objects.filter( Q(user_shop__in=usershops) | Q(partner_shop__in=usershops) ) )
        page = self.paginate_queryset(query)
        if page is not None:
            serializer = ExchangePartnerSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ExchangePartnerSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)







#end
