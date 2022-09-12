from rest_framework import serializers
from .models import PostWay, Address, ShippingTime, Cart, Order








#------------------------------------------------------------------------------
class ShippingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingTime
        fields = '__all__'





#------------------------------------------------------------------------------
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'





#------------------------------------------------------------------------------
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
