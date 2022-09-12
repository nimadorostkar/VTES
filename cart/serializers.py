from rest_framework import serializers
from .models import PostWay, Address, ShippingTime, Cart, Order











#------------------------------------------------------------------------------
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
