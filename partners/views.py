from django.shortcuts import render, get_object_or_404
from .serializers import ExchangePartnerSerializer
from rest_framework import viewsets, filters, status, pagination, mixins
from .models import ExchangePartner
from shop.models import Shop
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from django.db.models import Q













# ------------------------------------------------------- Partners -------------
class Partners(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        usershops = Shop.objects.filter(user=request.user)
        query = ExchangePartner.objects.filter( Q(user_shop__in=usershops) | Q(partner_shop__in=usershops) )
        serializer = ExchangePartnerSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data=request.data
        data['user_shop'] = Shop.objects.filter(user=request.user).first().id
        data['status'] = "در انتظار تایید"

        partnerExist = ExchangePartner.objects.filter( Q( user_shop=data['user_shop'], partner_shop=data['partner_shop'] ) | Q( user_shop=data['partner_shop'], partner_shop=data['user_shop']) )
        if partnerExist:
            return Response('فروشگاه مورد نظر در لیست همکاران شما موجود میباشد و یا درخواست همکاری پیش از این ارسال شده است', status=status.HTTP_400_BAD_REQUEST)

        serializer = ExchangePartnerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)














#End
