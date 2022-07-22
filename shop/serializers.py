from rest_framework import serializers
from .models import Shop, Product, Category, Brand, Attributes, ProductAttr, ProductImgs, ShopProducts, Attributes, ProductColor, Unit, City









#------------------------------------------------------------------------------
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'name')












#------------------------------------------------------------------------------
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')








#------------------------------------------------------------------------------
class MainCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')



class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)
    class Meta:
        model = Category
        fields=('id', 'name', 'children',)










#------------------------------------------------------------------------------
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'fname', 'link')










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
        fields = ('id', 'slug', 'name', 'user','user_mobile', 'phone', 'email', 'province', 'province_name', 'city', 'city_name', 'address', 'postal_code', 'lat_long', 'description','category', 'logo', 'cover', 'shaba_number', 'card_number', 'bank_account_number', 'instagram', 'linkedin', 'whatsapp', 'telegram', 'date_created')












#------------------------------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    #attributes = AttributesSerializer(read_only=True, many=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'code', 'irancode', 'approved', 'banner', 'brand', 'brand_name', 'link', 'category', 'category_name', 'description', 'datasheet', 'date_created')






class SearchSerializer(serializers.Serializer):
    q = serializers.CharField(max_length=64, allow_null=False)












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







#------------------------------------------------------------------------------
class ShopProductsSerializer(serializers.ModelSerializer):
    #attr = ProductAttrSerializer(many=True)
    #color = ProductColorSerializer(many=True)
    class Meta:
        model = ShopProducts
        fields = ('id' ,'available', 'shop','product', 'internal_code', 'qty', 'unit', 'price_model', 'one_price', 'medium_volume_price', 'medium_volume_qty', 'wholesale_volume_price', 'wholesale_volume_qty') #, 'attr', 'color'











#------------------------------------------------------------------------------
class MultiShopProductsSerializer(serializers.Serializer):
    products = serializers.CharField(max_length=100, allow_null=False)
    shop = serializers.CharField(max_length=30, allow_null=False)












#End
