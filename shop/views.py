from django.shortcuts import render, get_object_or_404
from .serializers import ( ShopSerializer, ProductSerializer, CategorySerializer,
                           ProductAttrSerializer, SearchSerializer, ProductImgsSerializer, MainCatSerializer,
                           ShopProductsSerializer, AttributesSerializer, ProductColorSerializer,
                           MultiShopProductsSerializer, BrandSerializer, UnitSerializer, CitySerializer )
from rest_framework import viewsets, filters, status, pagination, mixins
from .models import Shop, Product, Category , ProductAttr, ProductImgs, ShopProducts, Attributes, ProductColor, Unit
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











# --------------------------------------------------------- Brands -------------
class Brands(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        query = models.Brand.objects.all()
        serializer = BrandSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = AttributesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








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

        query = self.filter_queryset(Shop.objects.filter(category__in=category).distinct())
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
        shop = get_object_or_404(Shop, slug=self.kwargs["slug"])
        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        self.request.POST._mutable = True
        shop = get_object_or_404(Shop, slug=self.kwargs["slug"])
        req = request.data
        req['user'] = request.user.id
        serializer = ShopSerializer(shop, data=req)
        if serializer.is_valid():
            serializer.validated_data['category'] = [int(x) for x in req['category'].split(',')]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, slug=self.kwargs["slug"])
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
class Search(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ShopProductsSerializer
    pagination_class = CustomPagination
    queryset = ShopProducts.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['shop', 'product', 'available', 'product__category']
    search_fields = ['shop__name', 'product__name', 'internal_code']
    ordering_fields = ['id', 'available', 'product__name', 'product__code', 'product__id', 'product__date_created', 'product__brand', 'product__approved', 'shop__name', 'one_price']

    def get(self, request, format=None):

        if request.GET.get('category'):
            category_param = []
            cat_ids = [int(x) for x in request.GET.get('category').split(',')]
            for id in cat_ids:
                cat = Category.objects.get(id=id)
                cat_childs = cat.get_descendants(include_self=True)
                for C in cat_childs:
                    category_param.append(C.id)
        else:
            category_param = Category.objects.all().values_list('id', flat=True)

        allcolors=[]
        if request.GET.get('q'):
            search=request.GET.get('q')
        else:
            search=''

        if request.GET.get('maxp'):
            maxp=request.GET.get('maxp')
        else:
            maxp=999999999999

        if request.GET.get('minp'):
            minp=request.GET.get('minp')
        else:
            minp=0

        #----- color filter ----------------------
        productcolorfilter=[]
        if request.GET.get('color'):
            get_color_filter=request.GET.get('color')
            color_filter=[]
            for element in json.loads(get_color_filter):
                hexcolor = "#"+element
                color_filter.append(hexcolor)

            product_color = models.ProductColor.objects.filter(color__in=color_filter)
            for producttt in product_color:
                productcolorfilter.append(producttt.product.id)
        else:
            color_filter=None
        #----- end color filter ------------------


        product = models.Product.objects.filter( Q(name__icontains=search) | Q(description__icontains=search) | Q(brand__name__icontains=search) | Q(code__icontains=search) )
        shop = models.Shop.objects.filter( Q(name__icontains=search) | Q(description__icontains=search) | Q(phone__icontains=search) | Q(email__icontains=search) | Q(address__icontains=search) )
        shop_products = models.ShopProducts.objects.filter( Q(product__name__icontains=search) | Q(shop__name__icontains=search) | Q(product__description__icontains=search) | Q(shop__description__icontains=search) | Q(product__brand__name__icontains=search) | Q(product__brand__fname__icontains=search) | Q(product__code__icontains=search) | Q(product__irancode__icontains=search) )
        category = models.Category.objects.filter( Q(name__icontains=search) )

        product_serializer = ProductSerializer(product, many=True)
        shop_serializer = ShopSerializer(shop, many=True)
        category_serializer = CategorySerializer(category, many=True)

        #shop_products Start
        if productcolorfilter:
            shop_products_with_price=shop_products.filter(one_price__range=(minp, maxp))
            shop_products_with_price_colorfilter = shop_products_with_price.filter(id__in=productcolorfilter)
        else:
            shop_products_with_price_colorfilter=shop_products.filter(one_price__range=(minp, maxp))

        filtering_caaat =  shop_products_with_price_colorfilter.filter(product__category__id__in=category_param)

        query = self.filter_queryset(filtering_caaat)
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
                for QQ in attr_ids:
                    attribute=models.Attributes.objects.get(id=QQ)
                    values = []
                    for A in attr:
                        if A.attribute.id == QQ:
                            values.append(A.value)
                    attrvalue.append({ 'attribute':attribute.id, 'attribute_name':attribute.name, 'value':values })
                #print(attrvalue)
                color = models.ProductColor.objects.filter(product=Product)
                colors =[]
                for C in color.values_list('color', flat=True):
                    colors.append(C)
                    allcolors.append(C)
                #print(colors)

                if Product.product.brand.name:
                    brand_name = Product.product.brand.name
                    brand_fname = Product.product.brand.fname
                else:
                    brand_name = None
                    brand_fname = None

                productcat = Product.product.category
                if productcat.parent == None:
                    cat1 = { 'id':productcat.id, 'name':productcat.name }
                    cat2 = None
                    cat3 = None
                elif productcat.parent.parent == None:
                    cat1 = { 'id':productcat.parent.id, 'name':productcat.parent.name }
                    cat2 = { 'id':productcat.id, 'name':productcat.name }
                    cat3 = None
                elif productcat.parent.parent.parent == None:
                    cat1 = { 'id':productcat.parent.parent.id, 'name':productcat.parent.parent.name }
                    cat2 = { 'id':productcat.parent.id, 'name':productcat.parent.name }
                    cat3 = { 'id':productcat.id, 'name':productcat.name }
                else:
                    cat1 = None
                    cat2 = None
                    cat3 = None
                cat = {'cat1':cat1, 'cat2':cat2, 'cat3':cat3}


                product = { "id":Product.id, "product":Product.product.name, "productId":Product.product.id, "category":cat,
                      "shop":Product.shop.name, "shop_logo":Product.shop.logo.url, "shop_cover":Product.shop.cover.url,  "shopID":Product.shop.id, "image":Product.product.banner.url, "description":Product.product.description,
                      "available":Product.available, "internal_code":Product.internal_code, "brand":brand_name, "brand_fname":brand_fname, "link":Product.product.link,
                      "approved":Product.product.approved, "code":Product.product.code, "irancode":Product.product.irancode, "qty":Product.qty,
                      "price_model":Product.price_model, "one_price":Product.one_price, "medium_volume_price":Product.medium_volume_price,
                      "medium_volume_qty":Product.medium_volume_qty, "wholesale_volume_price":Product.wholesale_volume_price, "wholesale_volume_qty":Product.wholesale_volume_qty,
                      "attr": attrvalue, "color": colors }
                shopProduct.append(product)
            shopproductwithpage = self.get_paginated_response(shopProduct)
        #shop_products End

        if not query:
            max_min_price = { 'min':0, 'max':0 }
        else:
            maxprice = query.order_by('one_price').last()
            minprice = query.order_by('one_price').first()
            max_min_price = { 'min':minprice.one_price, 'max':maxprice.one_price }


        search_data={ "product":product_serializer.data , "shops":shop_serializer.data, "shop_products":shopproductwithpage.data, "shop_product_prices":max_min_price, "colors":list(set(allcolors)), "categories":category_serializer.data }
        return Response(search_data, status=status.HTTP_200_OK)












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













# ---------------------------------------------------- ShopProducts ------------

class ShopProducts(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ShopProductsSerializer
    pagination_class = CustomPagination
    queryset = ShopProducts.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['shop', 'product', 'available']
    search_fields = ['shop__name', 'product__name', 'internal_code']
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

                if Product.product.brand.name:
                    brand_name = Product.product.brand.name
                else:
                    brand_name = None


                productcat = Product.product.category
                if productcat.parent == None:
                    cat1 = { 'id':productcat.id, 'name':productcat.name }
                    cat2 = None
                    cat3 = None
                elif productcat.parent.parent == None:
                    cat1 = { 'id':productcat.parent.id, 'name':productcat.parent.name }
                    cat2 = { 'id':productcat.id, 'name':productcat.name }
                    cat3 = None
                elif productcat.parent.parent.parent == None:
                    cat1 = { 'id':productcat.parent.parent.id, 'name':productcat.parent.parent.name }
                    cat2 = { 'id':productcat.parent.id, 'name':productcat.parent.name }
                    cat3 = { 'id':productcat.id, 'name':productcat.name }
                else:
                    cat1 = None
                    cat2 = None
                    cat3 = None
                cat = {'cat1':cat1, 'cat2':cat2, 'cat3':cat3}


                product = { "id":Product.id, "product":Product.product.name, "productId":Product.product.id, "category":cat, "unit_id":Product.unit.id, "unit_name":Product.unit.name,
                      "shop":Product.shop.name,  "shopID":Product.shop.id, "image":Product.product.banner.url, "description":Product.product.description,
                      "available":Product.available, "internal_code":Product.internal_code, "brand":brand_name, "link":Product.product.link,
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
            product = { "id":Product.id, "product":Product.product.name, "productId":Product.product.id, "unit_id":Product.unit.id, "unit_name":Product.unit.name,
                  "shop":Product.shop.name,  "shopID":Product.shop.id, "image":Product.product.banner.url, "description":Product.product.description,
                  "available":Product.available, "internal_code":Product.internal_code, "brand":Product.product.brand.name, "link":Product.product.link,
                  "approved":Product.product.approved, "code":Product.product.code, "irancode":Product.product.irancode, "qty":Product.qty,
                  "price_model":Product.price_model, "one_price":Product.one_price, "medium_volume_price":Product.medium_volume_price,
                  "medium_volume_qty":Product.medium_volume_qty, "wholesale_volume_price":Product.wholesale_volume_price, "wholesale_volume_qty":Product.wholesale_volume_qty,
                  "attr": attrvalue, "color": colors }
            shopProduct.append(product)
        return Response(shopProduct, status=status.HTTP_200_OK)




    def post(self, request, format=None):
        self.request.POST._mutable = True
        data = request.data

        existcodes = models.Product.objects.all().values_list('code',flat=True).distinct()
        if data['code'] in existcodes:
            return Response('کد محصول تکراری می باشد', status=status.HTTP_400_BAD_REQUEST)
        else:
            product_serializer = ProductSerializer(data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
            else:
                print(product_serializer.errors)

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

        imgs = []
        product_imgs = models.ProductImgs.objects.filter(product=Product.product)
        for I in product_imgs:
            imgs.append(I.img.url)

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

        if Product.product.datasheet:
            datasheet = Product.product.datasheet.url
        else:
            datasheet = None


        productcat = Product.product.category
        if productcat.parent == None:
            cat1 = { 'id':productcat.id, 'name':productcat.name }
            cat2 = None
            cat3 = None
        elif productcat.parent.parent == None:
            cat1 = { 'id':productcat.parent.id, 'name':productcat.parent.name }
            cat2 = { 'id':productcat.id, 'name':productcat.name }
            cat3 = None
        elif productcat.parent.parent.parent == None:
            cat1 = { 'id':productcat.parent.parent.id, 'name':productcat.parent.parent.name }
            cat2 = { 'id':productcat.parent.id, 'name':productcat.parent.name }
            cat3 = { 'id':productcat.id, 'name':productcat.name }
        else:
            cat1 = None
            cat2 = None
            cat3 = None
        cat = {'cat1':cat1, 'cat2':cat2, 'cat3':cat3}


        shop_info = { "id":Product.shop.id, "user":Product.shop.user.mobile, "name":Product.shop.name, "phone":Product.shop.phone,
                      "email":Product.shop.email, "description":Product.shop.description, "category":Product.shop.category.all().values_list('id', 'name'),
                      "province":Product.shop.province.id, "province_name":Product.shop.province.name, "city":Product.shop.city.id, "city_name":Product.shop.city.name, "address":Product.shop.address, "postal_code":Product.shop.postal_code, "lat_long":Product.shop.lat_long,
                      "instagram":Product.shop.instagram, "linkedin":Product.shop.linkedin, "whatsapp":Product.shop.whatsapp, "telegram":Product.shop.telegram,
                      "logo":Product.shop.logo.url, "cover":Product.shop.cover.url }

        product_info = { "id":Product.product.id, "name":Product.product.name, "approved":Product.product.approved, "code":Product.product.code, "irancode":Product.product.irancode,
                         "brand_fname":Product.product.brand.fname, "brand_name":Product.product.brand.name, "brand_id":Product.product.brand.id, "link":Product.product.link, "description":Product.product.description,
                         "datasheet":datasheet, "banner":Product.product.banner.url, 'imgs':imgs, "category":cat  }

        general_info = { "id":Product.id, "available":Product.available, "qty":Product.qty, "price_model":Product.price_model, "internal_code":Product.internal_code, "unit":Product.unit.id, "unit_name":Product.unit.name,
                    "one_price":Product.one_price, "medium_volume_price":Product.medium_volume_price, "medium_volume_qty":Product.medium_volume_qty,
                    "wholesale_volume_price":Product.wholesale_volume_price, "wholesale_volume_qty":Product.wholesale_volume_qty,
                    "attr": attrvalue, "color": colors }

        data = { 'shop_info':shop_info, 'product_info':product_info, 'general_info':general_info }
        return Response(data, status=status.HTTP_200_OK)





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
                  "available":Product.available, "internal_code":Product.internal_code, "brand":Product.product.brand.id, "link":Product.product.link,
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








# -------------------------------------------------- SimilarProducts -----------
class SimilarProducts(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ShopProductsSerializer
    queryset = models.ShopProducts.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['shop', 'product', 'available']
    search_fields = ['shop__name', 'product__name', 'internal_code']
    ordering_fields = ['id', 'available', 'product__name', 'product__code', 'product__id', 'product__date_created', 'product__brand', 'product__approved', 'shop__name']

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(models.ShopProducts, id=self.kwargs["id"])
        similar_products = self.filter_queryset(models.ShopProducts.objects.filter(shop=product.shop, product__category=product.product.category))
        page = self.paginate_queryset(similar_products)
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

                if Product.product.brand.name:
                    brand_name = Product.product.brand.name
                else:
                    brand_name = None


                productcat = Product.product.category
                if productcat.parent == None:
                    cat1 = { 'id':productcat.id, 'name':productcat.name }
                    cat2 = None
                    cat3 = None
                elif productcat.parent.parent == None:
                    cat1 = { 'id':productcat.parent.id, 'name':productcat.parent.name }
                    cat2 = { 'id':productcat.id, 'name':productcat.name }
                    cat3 = None
                elif productcat.parent.parent.parent == None:
                    cat1 = { 'id':productcat.parent.parent.id, 'name':productcat.parent.parent.name }
                    cat2 = { 'id':productcat.parent.id, 'name':productcat.parent.name }
                    cat3 = { 'id':productcat.id, 'name':productcat.name }
                else:
                    cat1 = None
                    cat2 = None
                    cat3 = None
                cat = {'cat1':cat1, 'cat2':cat2, 'cat3':cat3}



                product = { "id":Product.id, "product":Product.product.name, "productId":Product.product.id, "category":cat,
                      "shop":Product.shop.name,  "shopID":Product.shop.id, "image":Product.product.banner.url, "description":Product.product.description,
                      "available":Product.available, "internal_code":Product.internal_code, "brand":brand_name, "link":Product.product.link,
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
                  "available":Product.available, "internal_code":Product.internal_code, "brand":Product.product.brand.name, "link":Product.product.link,
                  "approved":Product.product.approved, "code":Product.product.code, "irancode":Product.product.irancode, "qty":Product.qty,
                  "price_model":Product.price_model, "one_price":Product.one_price, "medium_volume_price":Product.medium_volume_price,
                  "medium_volume_qty":Product.medium_volume_qty, "wholesale_volume_price":Product.wholesale_volume_price, "wholesale_volume_qty":Product.wholesale_volume_qty,
                  "attr": attrvalue, "color": colors }
            shopProduct.append(product)
        return Response(shopProduct, status=status.HTTP_200_OK)


















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










# ------------------------------------------------------------- Units ---------

class Unit(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            units = models.Unit.objects.all()
            serializer = UnitSerializer(units, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)











# ---------------------------------------------------------- Provinces ---------
class Provinces(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            provinces = models.Province.objects.all()
            all_provinces=[]
            for Province in provinces:
                cities = models.City.objects.filter(province=Province)
                cities_serializer = CitySerializer(cities, many=True)
                province = {"id":Province.id, "name":Province.name, "cities":cities_serializer.data}
                all_provinces.append(province)
            return Response(all_provinces, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)









# ---------------------------------------------------------- ShopSlugs ---------
class ShopSlugs(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            slugs = models.Shop.objects.all().values_list('slug',flat=True)
            return Response(slugs, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)










# End
