from django.contrib.auth import login, authenticate, get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import MyUser
# from . import models
from . import forms
from . import helper
from django.contrib import messages
from .serializers import MyUserSerializer, RequestOTPSerializer, verifyOTPSerializer, UsersSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.views import generic
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.contrib.auth.signals import user_logged_in
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers






class MyUserView(APIView):
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
            user = MyUser.objects.get(mobile=mobile)  #user = get_object_or_404(MyUser, mobile=mobile)
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

        except MyUser.DoesNotExist:
            user=MyUser()
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






class verifyView(APIView):
    def get(self, request, **kwargs):
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = serializers.verifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)

        mobile = data['mobile']
        user = MyUser.objects.get(mobile=mobile)
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






class usersView(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    permission_classes = (AllowAny,) #https://testdriven.io/blog/built-in-permission-classes-drf/
    queryset = MyUser.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_legal', 'is_active', 'is_superuser', 'is_staff']
    search_fields = ['first_name', 'last_name', 'email', 'mobile', 'company', 'address']
    ordering_fields = ['date_joined', 'otp_create_time', 'last_login', 'id']






class ProfileAPI(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return MyUser.objects.filter(id=self.request.user.id)











#End
