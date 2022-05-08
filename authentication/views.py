from django.contrib.auth import login, authenticate, get_user_model, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import User
from . import forms
from . import helper
from django.contrib import messages
from .serializers import RequestOTPSerializer, verifyOTPSerializer, UsersSerializer, registerSerializer, ProfileImgSerializer
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
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from shop.models import Shop





# ------------------------------------------------------- Login ---------------

class Login(APIView):
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        serializer = serializers.RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data = serializer.errors)

        try:
            mobile = data['mobile']
            user = User.objects.get(mobile=mobile)

            if helper.check_send_otp(user.mobile):
                # send otp
                #otp = helper.get_random_otp()
                otp = '12345'
                print(otp)
                helper.otpsend(mobile, otp)
                #helper.send_otp_soap(mobile, otp)

                user.otp = otp
                user.save()
                return Response('کد تایید به شماره {} ارسال شد'.format(data['mobile']) , status=status.HTTP_200_OK)
            else:
                return Response('کد ارسال شده، لطفا ۲ دقیقه دیگر اقدام نمایید' , status=status.HTTP_408_REQUEST_TIMEOUT)

        except User.DoesNotExist:
            return Response('کاربری با شماره {} یافت نشد، لطفا ثبت نام کنید'.format(data['mobile']) , status=status.HTTP_400_BAD_REQUEST)





# ------------------------------------------------------- verifyView ---------------

class Verify(APIView):
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        serializer = serializers.verifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data = serializer.errors)

        mobile = data['mobile']
        user = User.objects.get(mobile=mobile)
        otp = data['otp']

        # check otp expiration
        if not helper.check_otp_expiration(user.mobile):
            return Response(data="کد منقضی شده است، لطفا دوباره امتحان کنید", status=status.HTTP_408_REQUEST_TIMEOUT)

        if user.otp != int(otp):
            return Response(data="کد اشتباه است", status=status.HTTP_417_EXPECTATION_FAILED)

        user.is_active = True
        user.save()

        token, created = Token.objects.get_or_create(user=user)
        print('API Auth Token: ', token.key)
        print('Created New Token:', created)

        user_shops = Shop.objects.filter(user=user)
        if user_shops.exists():
            has_a_shop = True
        else:
            has_a_shop = False

        user_data={"id":user.id, "first_name":user.first_name, "last_name":user.last_name, "image":user.image.url, "mobile":user.mobile, "is_legal":user.is_legal, "has_a_shop":has_a_shop, "company":user.company, "token": token.key}

        login(request, user)
        return Response(user_data, status=status.HTTP_200_OK)















# ------------------------------------------------------- Users ---------------

class Users(GenericAPIView):
    permission_classes = [IsAdminUser]
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    '''def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''







# ------------------------------------------------------- Profile ------------

class Profile(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(User, id=self.request.user.id)
        #serializer = UsersSerializer(profile)
        user_shops = Shop.objects.filter(user=profile)
        if user_shops.exists():
            has_a_shop = True
        else:
            has_a_shop = False

        user_data={"id":profile.id, "first_name":profile.first_name, "last_name":profile.last_name, "email":profile.email, "image":profile.image.url, "mobile":profile.mobile, "is_legal":profile.is_legal, "has_a_shop":has_a_shop, "address":profile.address, "company":profile.company, "email_verification":profile.email_verification, "referral_code":profile.referral_code}
        return Response(user_data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        profile = get_object_or_404(User, id=self.request.user.id)
        serializer = UsersSerializer(profile, data=request.data)
        #serializer.data.append(profile.password)
        if serializer.is_valid():
            serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, *args, **kwargs):
        profile = get_object_or_404(User, id=self.request.user.id)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def post(self, request, *args, **kwargs):
        try:
            file = request.data['file']
        except KeyError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        profile = get_object_or_404(User, id=self.request.user.id)
        profile.image = file
        profile.save()
        return Response(status=status.HTTP_200_OK)












# --------------------------------------------------------- logout ------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def Logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully', status=status.HTTP_401_UNAUTHORIZED)












# ------------------------------------------------------- Register ------------

class Register(APIView):
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        serializer = serializers.registerSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data = serializer.errors)


        try:
            mobile = data['mobile']
            user = User.objects.get(mobile=mobile)
            return Response('این شماره تلفن قبلا ثبت شده است', status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            user=User()
            user.is_legal = data['is_legal']

            if user.is_legal:
                user.mobile = data['mobile']
                user.company = data['company']
                user.email = data['email']
                user.address = data['address']
                user.referral_code = data['referral_code']
            else:
                user.mobile = data['mobile']
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.referral_code = data['referral_code']

            # send otp
            #otp = helper.get_random_otp()
            otp = '12345'
            helper.otpsend(mobile, otp)
            #helper.send_otp_soap(mobile, otp)
            # save otp
            print(otp)
            user.otp = otp
            user.is_active = False
            user.save()
            return Response('کد تایید به شماره {} ارسال شد'.format(user.mobile) , status=status.HTTP_200_OK)



















#End
