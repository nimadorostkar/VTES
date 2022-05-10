from rest_framework import serializers
from .models import ( Shop, Product, Category, Attributes,
                      ProductAttr, ProductImgs, ShopProducts,
                      Attributes, ProductColor )





#------------------------------------------------------------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')


#------------------------------------------------------------------------------
class MainCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')




class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
class CSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)
    class Meta:
        model = Category
        fields=('id', 'name', 'children',)










#------------------------------------------------------------------------------
class ProductAttrSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttr
        fields = ('id', 'product', 'product_name', 'attribute', 'attribute_name', 'value')






#------------------------------------------------------------------------------
class ProductImgsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImgs
        fields = ('id', 'product', 'product_name', 'img')







#------------------------------------------------------------------------------
class ShopSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    class Meta:
        model = Shop
        fields = ('id' ,'name', 'user','user_mobile', 'phone', 'email', 'country', 'city', 'address', 'postal_code', 'lat_long', 'description','category', 'logo', 'cover', 'shaba_number', 'card_number', 'bank_account_number', 'instagram', 'linkedin', 'whatsapp', 'telegram', 'date_created')










#------------------------------------------------------------------------------
class CreateShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('name', 'user', 'phone', 'email', 'country', 'city', 'address', 'postal_code', 'lat_long', 'description', 'logo', 'cover', 'shaba_number', 'card_number', 'bank_account_number', 'instagram', 'linkedin', 'whatsapp', 'telegram')









#------------------------------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    #attributes = AttributesSerializer(read_only=True, many=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'code', 'irancode', 'approved', 'banner', 'brand', 'link', 'category', 'category_name', 'description', 'datasheet', 'date_created')






class SearchSerializer(serializers.Serializer):
    q = serializers.CharField(max_length=64, allow_null=False)












#------------------------------------------------------------------------------
class ShopProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopProducts
        fields = ('id' ,'available', 'shop','product', 'internal_code', 'qty', 'price_model', 'one_price', 'two_price', 'min_two_qty', 'three_price', 'min_three_qty')







#------------------------------------------------------------------------------
class AttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = ('id', 'name')




#------------------------------------------------------------------------------
class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ('id', 'product', 'color')







#End
