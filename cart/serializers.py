from rest_framework import serializers
from .models import PostWay, Address, Cart, Order









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
