from rest_framework import serializers
from .models import Shop, Product, Product_Attr, Category , Attributes





class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id' ,'user', 'name', 'phone', 'email', 'address', 'description', 'category', 'logo', 'date_created')
