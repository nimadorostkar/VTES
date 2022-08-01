from django.shortcuts import render, get_object_or_404
from .models import Ticket
from . import models
from .serializers import TicketSerializer
from rest_framework import viewsets, filters, status, pagination, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView









#-------------------------------------------------------- Partners -------------
class Ticket(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tickets = models.Ticket.objects.filter(user=request.user).order_by('-created_date')
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        req = request.data
        req['user'] = request.user.id
        serializer = TicketSerializer(data=req)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)















#End
