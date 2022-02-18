from rest_framework import serializers
from .models import Shop, Product, Product_Attr, Category , Attributes





#------------------------------------------------------------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')




#------------------------------------------------------------------------------
class Product_AttrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Attr
        fields = ('id', 'product', 'attribute')




#------------------------------------------------------------------------------
class AttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = ('id', 'name')





#------------------------------------------------------------------------------
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id' ,'user', 'name', 'phone', 'email', 'address', 'description', 'category', 'logo', 'date_created')








#------------------------------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id' ,'approved', 'available', 'provider_shop', 'code', 'name', 'image', 'price', 'qty', 'brand', 'link', 'category', 'description', 'datasheet', 'date_created')
