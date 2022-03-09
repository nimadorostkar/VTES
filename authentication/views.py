from django.contrib.auth import login, authenticate, get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import User
from . import forms
from . import helper
from django.contrib import messages
from .serializers import RequestOTPSerializer, verifyOTPSerializer, UsersSerializer
from rest_framework import viewsets, filters, status, pagination, mixins
from django_filters.rest_framework import DjangoFilterBackend
from django.views import generic
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.contrib.auth.signals import user_logged_in
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from rest_framework.generics import GenericAPIView








# ------------------------------------------------------- Login ---------------

class Login(APIView):
    def get(self, request, **kwargs):
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = serializers.RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)

        try:
            mobile = data['mobile']      # request.POST.get('mobile') # mobile = request.POST['mobile']
            user = User.objects.get(mobile=mobile)  #user = get_object_or_404(MyUser, mobile=mobile)
            # send otp
            otp = helper.get_random_otp()
            print(otp)
            #helper.send_otp(mobile, otp)
            helper.send_otp_soap(mobile, otp)
            # save otp
            user.otp = otp
            user.save()
            #request.session['user_mobile'] = user.mobile
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            user=User()
            mobile = data['mobile']     # request.POST.get('mobile') #mobile = request.POST['mobile']
            user.mobile = mobile
            # send otp
            otp = helper.get_random_otp()
            #helper.send_otp(mobile, otp)
            helper.send_otp_soap(mobile, otp)
            # save otp
            print(otp)
            user.otp = otp
            user.is_active = False
            user.save()
            #request.session['user_mobile'] = user.mobile
            return Response(data=serializer.data, status=status.HTTP_200_OK)






# ------------------------------------------------------- verifyView ---------------

class Verify(APIView):
    def get(self, request, **kwargs):
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = serializers.verifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)

        mobile = data['mobile']
        user = User.objects.get(mobile=mobile)
        otp = data['otp']

        # check otp expiration
        if not helper.check_otp_expiration(user.mobile):
            return Response(data="OTP is expired, please try again.", status=status.HTTP_401_UNAUTHORIZED)

        if user.otp != int(otp):
            return Response(data="OTP is incorrect.", status=status.HTTP_401_UNAUTHORIZED)

        user.is_active = True
        user.save()
        login(request, user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)















# ------------------------------------------------------- Users ---------------

class Users(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_legal', 'is_active', 'is_superuser', 'is_staff']
    search_fields = ['first_name', 'last_name', 'email', 'mobile', 'company', 'address']
    ordering_fields = ['date_joined', 'otp_create_time', 'last_login', 'id']

    def get(self, request, format=None):
        queryset = User.objects.all()
        query = self.filter_queryset(User.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UsersSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# ------------------------------------------------------- Profile ------------

class Profile(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(User, id=self.request.user.id)
        serializer = UsersSerializer(profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        profile = get_object_or_404(User, id=self.request.user.id)
        serializer = UsersSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        profile = get_object_or_404(User, id=self.request.user.id)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)












#End
