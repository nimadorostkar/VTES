from rest_framework import serializers
from .models import PostWay, Address, Cart, Order











#------------------------------------------------------------------------------
class PostWaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostWay
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






#------------------------------------------------------------------------------
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'










#End
