from django.shortcuts import render, get_object_or_404
from .serializers import ( ShopSerializer, ProductSerializer, CategorySerializer,
                           ProductAttrSerializer, SearchSerializer, ProductImgsSerializer, MainCatSerializer,
                           ShopProductsSerializer, AttributesSerializer, ProductColorSerializer )
from rest_framework import viewsets, filters, status, pagination, mixins
from .models import Shop, Product, Category , ProductAttr, ProductImgs, ShopProducts, Attributes, ProductColor
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from . import serializers
from . import models
from django.db.models import Q





# ------------------------------------------------------- Attributes ------------
class Attributes(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AttributesSerializer
    queryset = Attributes.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['id']

    def get(self, request, format=None):
        query = self.filter_queryset(models.Attributes.objects.all())
        serializer = AttributesSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = AttributesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# ------------------------------------------------------- Attributes ------------
class Attrs(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductAttrSerializer
    queryset = ProductAttr.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['value','attribute']
    ordering_fields = ['id']

    def get(self, request, format=None):
        query = self.filter_queryset(ProductAttr.objects.all())
        serializer = ProductAttrSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ProductAttrSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttrsItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = ProductAttrSerializer

    def get(self, request, *args, **kwargs):
        attribute = get_object_or_404(ProductAttr, id=self.kwargs["id"])
        serializer = ProductAttrSerializer(attribute)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        attribute = get_object_or_404(ProductAttr, id=self.kwargs["id"])
        serializer = ProductAttrSerializer(attribute, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        attribute = get_object_or_404(ProductAttr, id=self.kwargs["id"])
        attribute.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)










# ---------------------------------------------------- Main Category ----------

class MainCat(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['id',]

    def get(self, request, format=None):
        query = self.filter_queryset(Category.objects.filter(mptt_level=0))
        serializer = MainCatSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)





# ------------------------------------------------------- Category ------------

class Categories(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent',]
    search_fields = ['name', 'parent']
    ordering_fields = ['id',]

    def get(self, request, format=None):
        query = self.filter_queryset(Category.objects.all())
        serializer = CategorySerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, id=self.kwargs["id"])
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        category = get_object_or_404(Category, id=self.kwargs["id"])
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        category = get_object_or_404(Category, id=self.kwargs["id"])
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)










# ------------------------------------------------------- Shops ------------

class Shops(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'category', 'city']
    search_fields = ['name', 'phone','email','address', 'description']
    ordering_fields = ['id', 'date_created']

    def get(self, request, format=None):
        queryset = Shop.objects.all()
        query = self.filter_queryset(Shop.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ShopSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            shop = request.data
            shop['user'] = request.user.id
            serializer = ShopSerializer(data = shop)
            if serializer.is_valid():
                serializer.save()
                S = Shop.objects.get(id=serializer.data['id'])
                for Q in [int(x) for x in shop['category'].split(',')]:
                    S.category.add(Category.objects.get(id=Q))
                S.save()

                data = {'id':S.id, 'name':S.name, 'phone':S.phone, 'email':S.email, 'city':S.city,
                        'address':S.address, 'postal_code':S.postal_code, 'lat_long':S.lat_long,
                        'logo':S.logo.url, 'cover':S.cover.url, 'description':S.description, 'shaba_number':S.shaba_number,
                        'card_number':S.card_number, 'bank_account_number':S.bank_account_number, 'linkedin':S.linkedin,
                        'instagram':S.instagram, 'whatsapp':S.whatsapp, 'telegram':S.telegram }
                return Response(data, status=status.HTTP_201_CREATED)

        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class ShopItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = ShopSerializer

    def get(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, id=self.kwargs["id"])
        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, id=self.kwargs["id"])
        req = request.data
        req['user'] = request.user.id
        serializer = ShopSerializer(shop, data=req)
        if serializer.is_valid():
            serializer.save()
            for Q in [int(x) for x in req['category'].split(',')]:
                shop.category.add(Category.objects.get(id=Q))
            shop.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, id=self.kwargs["id"])
        shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)












# ------------------------------------------------------- Products ------------

class Products(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'approved', 'brand']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['id', 'date_created']

    def get(self, request, format=None):
        queryset = Product.objects.all()
        query = self.filter_queryset(Product.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProductSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs["id"])
        serializer = ProductSerializer(product)
        product_img = ProductImgs.objects.filter(product=product)
        imgs = []
        for img in product_img:
            imgs.append(img.img.url)
        data={ "product":serializer.data, "images":imgs }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs["id"])
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs["id"])
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)









# ------------------------------------------------------- Search ------------

class Search(APIView):
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        return Response( 'please use POST method, and send query for search' , status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        serializer = serializers.SearchSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response('There is a problem with the submitted information, please resend query',status=status.HTTP_400_BAD_REQUEST)
        search = data['q']
        if search:
            product = models.Product.objects.filter( Q(name__icontains=search) | Q(description__icontains=search) | Q(brand__icontains=search) | Q(code__icontains=search) )
            shop = models.Shop.objects.filter( Q(name__icontains=search) | Q(description__icontains=search) | Q(phone__icontains=search) | Q(email__icontains=search) | Q(address__icontains=search) )
            category = models.Category.objects.filter( Q(name__icontains=search) )

            product_serializer = ProductSerializer(product, many=True)
            shop_serializer = ShopSerializer(shop, many=True)
            category_serializer = CategorySerializer(category, many=True)

            search_data={ "product":product_serializer.data , "shops":shop_serializer.data, "categories":category_serializer.data }
            return Response(search_data, status=status.HTTP_200_OK)
        else:
            return Response('please send query for search', status=status.HTTP_400_BAD_REQUEST)














# ------------------------------------------------------- Attributes ------------

class ProductImg(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductImgsSerializer
    queryset = ProductImgs.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product',]
    search_fields = ['product',]
    ordering_fields = ['id',]

    def get(self, request, format=None):
        queryset = ProductImgs.objects.all()
        query = self.filter_queryset(ProductImgs.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProductImgsSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductImgsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)













# ------------------------------------------------------- Products ------------

class ShopProducts(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ShopProductsSerializer
    queryset = ShopProducts.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['shop', 'product', 'available']
    search_fields = ['shop__name', 'product__name', 'internal_code']
    ordering_fields = ['id']

    def get(self, request, format=None):
        query = self.filter_queryset(models.ShopProducts.objects.all())
        shopProduct=[]
        for Product in query:
            attr = models.ProductAttr.objects.filter(product=Product)
            attr_serializer = ProductAttrSerializer(attr, many=True)
            color = models.ProductColor.objects.filter(product=Product)
            color_serializer = ProductColorSerializer(color, many=True)
            product = { "id":Product.id, "product":Product.product.name, "productId":Product.product.id,
                  "shop":Product.shop.name,  "shopID":Product.shop.id,
                  "available":Product.available, "internal_code":Product.internal_code, "brand":Product.product.brand,
                  "approved":Product.product.approved, "code":Product.product.code, "irancode":Product.product.irancode, "qty":Product.qty,
                  "price_model":Product.price_model, "one_price":Product.one_price, "medium_volume_price":Product.medium_volume_price,
                  "medium_volume_qty":Product.medium_volume_qty, "wholesale_volume_price":Product.wholesale_volume_price, "wholesale_volume_qty":Product.wholesale_volume_qty,
                  "attr": attr_serializer.data, "color": color_serializer.data }
            shopProduct.append(product)
        return Response(shopProduct, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ShopProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopProductsItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ShopProductsSerializer

    def get(self, request, *args, **kwargs):
        Product = get_object_or_404(models.ShopProducts, id=self.kwargs["id"])
        serializer = ShopProductsSerializer(Product)
        attr = models.ProductAttr.objects.filter(product=Product)
        attr_serializer = ProductAttrSerializer(attr, many=True)
        color = models.ProductColor.objects.filter(product=Product)
        color_serializer = ProductColorSerializer(color, many=True)
        product = { "id":Product.id, "product":Product.product.name, "productId":Product.product.id,
              "shop":Product.shop.name,  "shopID":Product.shop.id,
              "available":Product.available, "internal_code":Product.internal_code, "qty":Product.qty,
              "price_model":Product.price_model, "one_price":Product.one_price, "medium_volume_price":Product.medium_volume_price,
              "medium_volume_qty":Product.medium_volume_qty, "wholesale_volume_price":Product.wholesale_volume_price, "wholesale_volume_qty":Product.wholesale_volume_qty,
              "attr": attr_serializer.data, "color": color_serializer.data }
        return Response(product, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        shop_product = get_object_or_404(models.ShopProducts, id=self.kwargs["id"])
        serializer = ShopProductsSerializer(shop_product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        shop_product = get_object_or_404(models.ShopProducts, id=self.kwargs["id"])
        shop_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# ------------------------------------------------ ShopProductsDelete ---------

class ShopProductsDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data['products']
        products_id = [int(x) for x in data.split(',')]

        try:
            for Q in products_id:
                shop_product = models.ShopProducts.objects.get(id=Q)
                if shop_product.shop.user == request.user:
                    shop_product.delete()
            return Response(status=status.HTTP_200_OK)

        except:
            return Response('Something went wrong please try again and check shop_products IDs', status=status.HTTP_400_BAD_REQUEST)















'''
    def post(self, request, format=None):
        try:
            shop = Shop()
            shop.user = request.user
            shop.name = request.data['name']
            shop.phone = request.data['phone']
            shop.email = request.data['email']
            shop.city = request.data['city']
            shop.address = request.data['address']
            shop.postal_code = request.data['postal_code']
            shop.lat_long = request.data['lat_long']
            shop.description = request.data['description']
            shop.logo = request.data['logo']
            shop.cover = request.data['cover']
            shop.shaba_number = request.data['shaba_number']
            shop.card_number = request.data['card_number']
            shop.bank_account_number = request.data['bank_account_number']
            shop.instagram = request.data['instagram']
            shop.linkedin = request.data['linkedin']
            shop.whatsapp = request.data['whatsapp']
            shop.telegram = request.data['telegram']
            shop.save()
            for Q in [int(x) for x in request.data['category'].split(',')]:
                shop.category.add(Category.objects.get(id=Q))
                shop.save()

            data = { 'id':shop.id, 'user':shop.user, 'name':shop.name, 'phone':shop.phone, 'email':shop.email, 'city':shop.city,
                     'address':shop.address, 'postal_code':shop.postal_code, 'lat_long':shop.lat_long,
                     'logo':shop.logo.url, 'cover':shop.cover.url, 'description':shop.description, 'shaba_number':shop.shaba_number,
                     'card_number':shop.card_number, 'bank_account_number':shop.bank_account_number, 'linkedin':shop.linkedin,
                     'instagram':shop.instagram, 'whatsapp':shop.whatsapp, 'telegram':shop.telegram }


            return Response(shop.id, status=status.HTTP_201_CREATED)

        except:
            return Response('There is a problem, please try again. Make sure all fields are submitted',status=status.HTTP_400_BAD_REQUEST)

        #print(shop['category'])
        #cat = Category.objects.filter(id__in=[int(x) for x in shop['category'].split(',')])
        #print(cat)
        #cat_serializer = CatSerializer(cat, many=True)
        #print(cat_serializer)

        #for Q in [int(x) for x in shop['category'].split(',')]:
            #S.category.add(Category.objects.get(id=Q))


        #cat = Category.objects.filter(id__in=[int(x) for x in shop['category'].split(',')])
        #cat_serializer = ShopSerializer(data = cat)
        #shop['category'] = cat_serializer
        #serializer = ShopSerializer(data = shop)
        #if serializer.is_valid():
            #serializer.save()
'''










# End
