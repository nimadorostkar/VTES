from rest_framework import serializers
from .models import User




class RequestOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=64, allow_null=False)




class verifyOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=64, allow_null=False)
    otp = serializers.CharField(max_length=5, allow_null=False)




class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'mobile', 'otp', 'is_legal', 'company', 'email_verification', 'address', 'referral_code', 'image', )
        #fields = '__all__'




class ProfileImgSerializer(serializers.Serializer):
    image = serializers.ImageField(max_length=None,use_url=True)







class registerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('mobile' ,'is_legal', 'first_name','last_name', 'company', 'email', 'address', 'referral_code')
