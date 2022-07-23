from django.shortcuts import render, get_object_or_404
#from .serializers import Partners
from rest_framework import viewsets, filters, status, pagination, mixins
from .models import ExchangePartner
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
        query = ExchangePartner.objects.filter( Q(user_shop=request.user) | Q(partner_shop=request.user) )
        serializer = BrandSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = AttributesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)














#End
