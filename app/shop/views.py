from django.shortcuts import render, get_object_or_404
from .serializers import ( ShopSerializer, ProductSerializer, CategorySerializer,
                           ProductAttrSerializer, SearchSerializer, ProductImgsSerializer, MainCatSerializer,
                           ShopProductsSerializer, AttributesSerializer, ProductColorSerializer, MultiShopProductsSerializer )
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
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import pagination

import json


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100










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
        query = self.filter_queryset(Category.objects.filter(mptt_level=0))
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
    pagination_class = CustomPagination
    queryset = Shop.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'city']
    search_fields = ['name', 'phone','email','address', 'description']
    ordering_fields = ['id', 'date_created']

    def get(self, request, format=None):

        if request.GET.get('category'):
            category = []
            cat_ids = [int(x) for x in request.GET.get('category').split(',')]
            for id in cat_ids:
                cat = Category.objects.get(id=id)
                cat_childs = cat.get_descendants(include_self=True)
                for C in cat_childs:
                    category.append(C.id)
        else:
            category = Category.objects.all()

        query = self.filter_queryset(Shop.objects.filter(category__in=category))
        page = self.paginate_queryset(query)
        if page is not None:
            #serializer = self.get_serializer(page, many=True)
            serializer = ShopSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ShopSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        self.request.POST._mutable = True
        req = request.data
        req['user'] = request.user.id
        serializer = ShopSerializer(data=req)
        if serializer.is_valid():
            serializer.validated_data['category'] = [int(x) for x in req['category'].split(',')]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ShopItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = ShopSerializer

    def get(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, id=self.kwargs["id"])
        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        self.request.POST._mutable = True
        shop = get_object_or_404(Shop, id=self.kwargs["id"])
        req = request.data
        req['user'] = request.user.id
        serializer = ShopSerializer(shop, data=req)
        if serializer.is_valid():
            serializer.validated_data['category'] = [int(x) for x in req['category'].split(',')]
            serializer.save()
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
    pagination_class = CustomPagination
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['approved', 'brand']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['id', 'date_created', 'name', 'brand', 'code', 'approved']

    def get(self, request, format=None):

        if request.GET.get('category'):
            category = []
            cat_ids = [int(x) for x in request.GET.get('category').split(',')]
            for id in cat_ids:
                cat = Category.objects.get(id=id)
                cat_childs = cat.get_descendants(include_self=True)
                for C in cat_childs:
                    category.append(C.id)
        else:
            category = Category.objects.all()

        query = self.filter_queryset(Product.objects.filter(category__in=category))
        page = self.paginate_queryset(query)
        if page is not None:
            #serializer = self.get_serializer(page, many=True)
            serializer = ProductSerializer(page, many=True)
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
            shop_products = models.ShopProducts.objects.filter( Q(product__name__icontains=search) | Q(shop__name__icontains=search) | Q(product__description__icontains=search) | Q(shop__description__icontains=search) | Q(product__brand__icontains=search) | Q(product__code__icontains=search) | Q(product__irancode__icontains=search) )
            category = models.Category.objects.filter( Q(name__icontains=search) )

            product_serializer = ProductSerializer(product, many=True)
            shop_serializer = ShopSerializer(shop, many=True)
            shop_products_serializer = ShopProductsSerializer(shop_products, many=True)
            category_serializer = CategorySerializer(category, many=True)

            search_data={ "product":product_serializer.data , "shops":shop_serializer.data, "shop_products":shop_products_serializer.data, "categories":category_serializer.data }
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
    pagination_class = CustomPagination
    queryset = ShopProducts.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['shop', 'product', 'available']
    search_fields = ['shop__name', 'product__name', 'product__brand', 'internal_code']
    ordering_fields = ['id', 'available', 'product__name', 'product__code', 'product__id', 'product__date_created', 'product__brand', 'product__approved', 'shop__name']

    def get(self, request, format=None):
        query = self.filter_queryset(models.ShopProducts.objects.all())
        page = self.paginate_queryset(query)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            shopProduct=[]
            for Product in page:
                attr = models.ProductAttr.objects.filter(product=Product)
                attr_serializer = ProductAttrSerializer(attr, many=True)

                just_attr = []
                for AA in attr_serializer.data:
                    just_attr.append(AA['attribute'])
                attr_ids = list(set(just_attr))

                attrvalue = []
                for Q in attr_ids:
                    attribute=models.Attributes.objects.get(id=Q)
                    values = []
                    for A in attr:
                        if A.attribute.id == Q:
                            values.append(A.value)
                    attrvalue.append({ 'attribute':attribute.id, 'attribute_name':attribute.name, 'value':values })
                #print(attrvalue)

                color = models.ProductColor.objects.filter(product=Product)
                colors =[]
                for C in color.values_list('color', flat=True):
                    colors.append(C)
                #print(colors)

                product = { "id":Product.id, "product":Product.product.name, "productId":Product.product.id,
                      "shop":Product.shop.name,  "shopID":Product.shop.id, "image":Product.product.banner.url, "description":Product.product.description,
                      "available":Product.available, "internal_code":Product.internal_code, "brand":Product.product.brand, "link":Product.product.link,
                      "approved":Product.product.approved, "code":Product.product.code, "irancode":Product.product.irancode, "qty":Product.qty,
                      "price_model":Product.price_model, "one_price":Product.one_price, "medium_volume_price":Product.medium_volume_price,
                      "medium_volume_qty":Product.medium_volume_qty, "wholesale_volume_price":Product.wholesale_volume_price, "wholesale_volume_qty":Product.wholesale_volume_qty,
                      "attr": attrvalue, "color": colors }
                shopProduct.append(product)
            return self.get_paginated_response(shopProduct)

        shopProduct=[]
        for Product in query:
            attr = models.ProductAttr.objects.filter(product=Product)
            attr_serializer = ProductAttrSerializer(attr, many=True)
            color = models.ProductColor.objects.filter(product=Product)
            color_serializer = ProductColorSerializer(color, many=True)
            product = { "id":Product.id, "product":Product.product.name, "productId":Product.product.id,
                  "shop":Product.shop.name,  "shopID":Product.shop.id, "image":Product.product.banner.url, "description":Product.product.description,
                  "available":Product.available, "internal_code":Product.internal_code, "brand":Product.product.brand, "link":Product.product.link,
                  "approved":Product.product.approved, "code":Product.product.code, "irancode":Product.product.irancode, "qty":Product.qty,
                  "price_model":Product.price_model, "one_price":Product.one_price, "medium_volume_price":Product.medium_volume_price,
                  "medium_volume_qty":Product.medium_volume_qty, "wholesale_volume_price":Product.wholesale_volume_price, "wholesale_volume_qty":Product.wholesale_volume_qty,
                  "attr": attrvalue, "color": colors }
            shopProduct.append(product)
        return Response(shopProduct, status=status.HTTP_200_OK)




    def post(self, request, format=None):
        self.request.POST._mutable = True
        data = request.data

        product_serializer = ProductSerializer(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()

        data['product'] = product_serializer.data['id']

        shop_serializer = ShopProductsSerializer(data=request.data)
        if shop_serializer.is_valid():
            shop_serializer.save()

        color_data = json.loads(data['colors'])
        color = models.ProductColor.objects.filter(product=models.ShopProducts.objects.get(id=shop_serializer.data['id']))
        color.delete()
        for C in color_data:
            newcolor = ProductColor()
            newcolor.product= models.ShopProducts.objects.get(id=shop_serializer.data['id'])
            newcolor.color=C
            newcolor.save()

        attr_data = json.loads(data['attr'])
        attrs = models.ProductAttr.objects.filter(product=shop_serializer.data['id'])
        attrs.delete()
        for attr in attr_data:
            for val in attr['value']:
                newattr = ProductAttr()
                newattr.product= models.ShopProducts.objects.get(id=shop_serializer.data['id'])
                obj, created = models.Attributes.objects.get_or_create(name=attr['name'])
                newattr.attribute = models.Attributes.objects.get(id=obj.id)
                newattr.value = val
                newattr.save()

        if data['img1']:
            img = ProductImgs()
            img.product = Product.objects.get(id=data['product'])
            img.img = data['img1']
            img.save()

        if data['img2']:
            img = ProductImgs()
            img.product = Product.objects.get(id=data['product'])
            img.img = data['img2']
            img.save()

        if data['img3']:
            img = ProductImgs()
            img.product = Product.objects.get(id=data['product'])
            img.img = data['img3']
            img.save()

        if data['img4']:
            img = ProductImgs()
            img.product = Product.objects.get(id=data['product'])
            img.img = data['img4']
            img.save()

        if data['img5']:
            img = ProductImgs()
            img.product = Product.objects.get(id=data['product'])
            img.img = data['img5']
            img.save()

        if data['img6']:
            img = ProductImgs()
            img.product = Product.objects.get(id=data['product'])
            img.img = data['img6']
            img.save()

        return Response(shop_serializer.data['id'], status=status.HTTP_200_OK)












class ShopProductsItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ShopProductsSerializer

    def get(self, request, *args, **kwargs):
        Product = get_object_or_404(models.ShopProducts, id=self.kwargs["id"])
        serializer = ShopProductsSerializer(Product)
        attr = models.ProductAttr.objects.filter(product=Product)
        attr_serializer = ProductAttrSerializer(attr, many=True)

        color = models.ProductColor.objects.filter(product=Product)
        colors =[]
        for C in color.values_list('color', flat=True):
            colors.append(C)
        #print(colors)

        just_attr = []
        for AA in attr_serializer.data:
            just_attr.append(AA['attribute'])
        attr_ids = list(set(just_attr))

        attrvalue = []
        for Q in attr_ids:
            attribute=models.Attributes.objects.get(id=Q)
            values = []
            for A in attr:
                if A.attribute.id == Q:
                    values.append(A.value)
            attrvalue.append({ 'attribute':attribute.id, 'attribute_name':attribute.name, 'value':values })
        #print(attrvalue)
        product = { "id":Product.id, "product":Product.product.name, "productId":Product.product.id,
              "shop":Product.shop.name,  "shopID":Product.shop.id, "image":Product.product.banner.url, "description":Product.product.description,
              "available":Product.available, "internal_code":Product.internal_code, "brand":Product.product.brand, "link":Product.product.link,
              "approved":Product.product.approved, "code":Product.product.code, "irancode":Product.product.irancode, "qty":Product.qty,
              "price_model":Product.price_model, "one_price":Product.one_price, "medium_volume_price":Product.medium_volume_price,
              "medium_volume_qty":Product.medium_volume_qty, "wholesale_volume_price":Product.wholesale_volume_price, "wholesale_volume_qty":Product.wholesale_volume_qty,
              "attr": attrvalue, "color": colors }

        return Response(product, status=status.HTTP_200_OK)





    def put(self, request, *args, **kwargs):
        shop_product = get_object_or_404(models.ShopProducts, id=self.kwargs["id"])
        data=request.data
        data['product'] = shop_product.product.id
        data['shop'] = shop_product.shop.id

        color = models.ProductColor.objects.filter(product=shop_product)
        color.delete()
        for C in data['colors']:
            newcolor = ProductColor()
            newcolor.product=shop_product
            newcolor.color=C
            newcolor.save()

        attrs = models.ProductAttr.objects.filter(product=shop_product)
        attrs.delete()
        for attr in data['attr']:
            for val in attr['value']:
                newattr = ProductAttr()
                newattr.product=shop_product
                obj, created = models.Attributes.objects.get_or_create(name=attr['name'])
                newattr.attribute = models.Attributes.objects.get(id=obj.id)
                newattr.value = val
                newattr.save()

        serializer = ShopProductsSerializer(shop_product, data=data)
        if serializer.is_valid():
            serializer.save()

            Product = get_object_or_404(models.ShopProducts, id=self.kwargs["id"])
            color = models.ProductColor.objects.filter(product=Product)
            colors =[]
            for C in color.values_list('color', flat=True):
                colors.append(C)
            #print(colors)

            attr = models.ProductAttr.objects.filter(product=Product)
            attr_serializer = ProductAttrSerializer(attr, many=True)
            just_attr = []
            for AA in attr_serializer.data:
                just_attr.append(AA['attribute'])
            attr_ids = list(set(just_attr))

            attrvalue = []
            for Q in attr_ids:
                attribute=models.Attributes.objects.get(id=Q)
                values = []
                for A in attr:
                    if A.attribute.id == Q:
                        values.append(A.value)
                attrvalue.append({ 'attribute':attribute.id, 'attribute_name':attribute.name, 'value':values })
            #print(attrvalue)
            product = { "id":Product.id, "product":Product.product.name, "productId":Product.product.id,
                  "shop":Product.shop.name,  "shopID":Product.shop.id, "image":Product.product.banner.url, "description":Product.product.description,
                  "available":Product.available, "internal_code":Product.internal_code, "brand":Product.product.brand, "link":Product.product.link,
                  "approved":Product.product.approved, "code":Product.product.code, "irancode":Product.product.irancode, "qty":Product.qty,
                  "price_model":Product.price_model, "one_price":Product.one_price, "medium_volume_price":Product.medium_volume_price,
                  "medium_volume_qty":Product.medium_volume_qty, "wholesale_volume_price":Product.wholesale_volume_price, "wholesale_volume_qty":Product.wholesale_volume_qty,
                  "attr": attrvalue, "color": colors }

            return Response(product, status=status.HTTP_201_CREATED)
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









# ------------------------------------------------------- Products ------------

class MultiShopProductsAdd(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = serializers.MultiShopProductsSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            shop = Shop.objects.get(id=data['shop'])
            products_id = [int(x) for x in data['products'].split(',')]

            exists = []
            for P in products_id:
                if models.ShopProducts.objects.filter(shop=shop,product__id=P).exists():
                    exists.append(P)
            if exists:
                return Response(exists, status=status.HTTP_400_BAD_REQUEST)


            added_products = []
            for Q in products_id:
                data['product'] = Q
                shopproduct = ShopProductsSerializer(data=data)
                if shopproduct.is_valid():
                    shopproduct.save()
                    added_products.append(shopproduct.data)
            return Response(added_products, status=status.HTTP_200_OK)
        except:
            return Response('مشکلی رخ داده است ، شناسه  فروشگاه و محصولات را بررسی کنید',status=status.HTTP_400_BAD_REQUEST)











# ------------------------------------------------------- Attributes ------------

class Color(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductColorSerializer
    #queryset = ProductImgs.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product',]
    search_fields = ['product', 'color']
    ordering_fields = ['id',]

    def get(self, request, format=None):
        query = self.filter_queryset(ProductColor.objects.all())
        serializer = ProductColorSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ProductColorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
















# End
