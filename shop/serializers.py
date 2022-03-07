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
        fields = ('id', 'product','product_name', 'attribute', 'attribute_name')




#------------------------------------------------------------------------------
class AttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = ('id', 'name')





#------------------------------------------------------------------------------
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id' ,'name', 'user','user_mobile', 'phone', 'email', 'address', 'description', 'category', 'category_name', 'logo', 'date_created')







'''
#------------------------------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'id', 'code', 'approved', 'available', 'provider_shop', 'provider_shop_name', 'image', 'price', 'qty', 'brand', 'link', 'category', 'category_name', 'description', 'datasheet', 'date_created')
'''

#------------------------------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'code', 'approved', 'available', 'provider_shop', 'provider_shop_name', 'image', 'price', 'qty', 'brand', 'link', 'category', 'category_name', 'description', 'datasheet', 'date_created')










#End
