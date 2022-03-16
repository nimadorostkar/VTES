from rest_framework import serializers
from .models import Shop, Product, Category, Attributes, ProductAttr





#------------------------------------------------------------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')



'''
#------------------------------------------------------------------------------
class AttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = ('id', 'name')
'''




#------------------------------------------------------------------------------
class ProductAttrSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttr
        fields = ('id', 'product', 'product_name', 'attribute', 'attribute_name', 'value')






#------------------------------------------------------------------------------
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id' ,'name', 'user','user_mobile', 'phone', 'email', 'address', 'description', 'category', 'category_name', 'logo', 'date_created')







#------------------------------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    #attributes = AttributesSerializer(read_only=True, many=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'code', 'approved', 'available', 'provider_shop', 'provider_shop_name', 'image', 'single_price', 'overall_price', 'qty', 'brand', 'link', 'category', 'category_name', 'description', 'datasheet', 'date_created')










#End
