from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .serializers import ExchangePartnerSerializer
from rest_framework import viewsets, filters, status, pagination, mixins
from .models import ExchangePartner
from shop.models import Shop, Product, Category , ProductAttr, ProductImgs, ShopProducts, Attributes, ProductColor, Unit
from shop import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import pagination
import json
from shop.serializers import ( ShopSerializer, ProductSerializer, CategorySerializer,
                           ProductAttrSerializer, SearchSerializer, ProductImgsSerializer, MainCatSerializer,
                           ShopProductsSerializer, AttributesSerializer, ProductColorSerializer,
                           MultiShopProductsSerializer, BrandSerializer, UnitSerializer, CitySerializer )




class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100













#-------------------------------------------------------- Partners -------------
class Partners(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        usershops = Shop.objects.filter(user=request.user)
        query = ExchangePartner.objects.filter( Q(user_shop__in=usershops) | Q(partner_shop__in=usershops) )
        serializer = ExchangePartnerSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        data=request.data
        data['user_shop'] = Shop.objects.filter(user=request.user).first().id
        data['status'] = "در انتظار تایید"

        partnerExist = ExchangePartner.objects.filter( Q( user_shop=data['user_shop'], partner_shop=data['partner_shop'] ) | Q( user_shop=data['partner_shop'], partner_shop=data['user_shop']) )
        if partnerExist:
            return Response('فروشگاه مورد نظر در لیست همکاران شما موجود میباشد و یا درخواست همکاری پیش از این ارسال شده است', status=status.HTTP_400_BAD_REQUEST)

        serializer = ExchangePartnerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









#----------------------------------------------------- PartnerItem -------------
class PartnerItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        partner = ExchangePartner.objects.get(id=self.kwargs["id"])
        serializer = ExchangePartnerSerializer(partner)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        partner = ExchangePartner.objects.get(id=self.kwargs["id"])
        serializer = ExchangePartnerSerializer(partner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        partner = ExchangePartner.objects.get(id=self.kwargs["id"])
        partner.delete()
        return Response(status=status.HTTP_200_OK)


















#------------------------------------------------ PartnersProducts -------------
class PartnersProducts(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ShopProductsSerializer
    pagination_class = CustomPagination
    queryset = ShopProducts.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['shop', 'product', 'available', 'shop__slug']
    search_fields = ['shop__name', 'product__name', 'internal_code']
    ordering_fields = ['id', 'slug', 'available', 'product__name', 'product__code', 'product__id', 'product__date_created', 'product__brand', 'product__approved', 'shop__name']

    def get(self, request, format=None):

        usershops = Shop.objects.filter(user=request.user)
        partner_shops = ExchangePartner.objects.filter( Q(user_shop__in=usershops) | Q(partner_shop__in=usershops) )
        print('----------')
        print(partner_shops)

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

                if Product.unit:
                    p_unit_id = Product.unit.id
                    p_unit_name = Product.unit.name
                else:
                    p_unit_id = None
                    p_unit_name = None




                product = { "id":Product.id, "product":Product.product.name, "productId":Product.product.id, "category":cat, "unit_id":p_unit_id, "unit_name":p_unit_name,
                      "shop":Product.shop.name, "shop_slug":Product.shop.slug,  "shopID":Product.shop.id, "image":Product.product.banner.url, "description":Product.product.description,
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
            product = { "id":Product.id, "product":Product.product.name, "productId":Product.product.id, "unit_id":p_unit_id, "unit_name":p_unit_name,
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
















#-------------------------------------------------- PartnerProduct -------------
class PartnerProduct(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
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


        if Product.product.category:
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
        else:
            cat=None



        if Product.unit:
            p_unit_id = Product.unit.id
            p_unit_name = Product.unit.name
        else:
            p_unit_id = None
            p_unit_name = None


        shop_info = { "id":Product.shop.id, "slug":Product.shop.slug, "user":Product.shop.user.mobile, "name":Product.shop.name, "phone":Product.shop.phone,
                      "email":Product.shop.email, "description":Product.shop.description, "category":Product.shop.category.all().values_list('id', 'name'),
                      "province":Product.shop.province.id, "province_name":Product.shop.province.name, "city":Product.shop.city.id, "city_name":Product.shop.city.name, "address":Product.shop.address, "postal_code":Product.shop.postal_code, "lat_long":Product.shop.lat_long,
                      "instagram":Product.shop.instagram, "linkedin":Product.shop.linkedin, "whatsapp":Product.shop.whatsapp, "telegram":Product.shop.telegram,
                      "logo":Product.shop.logo.url, "cover":Product.shop.cover.url }

        product_info = { "id":Product.product.id, "name":Product.product.name, "approved":Product.product.approved, "code":Product.product.code, "irancode":Product.product.irancode,
                         "brand_fname":Product.product.brand.fname, "brand_name":Product.product.brand.name, "brand_id":Product.product.brand.id, "link":Product.product.link, "description":Product.product.description,
                         "datasheet":datasheet, "banner":Product.product.banner.url, 'imgs':imgs, "category":cat  }

        general_info = { "id":Product.id, "available":Product.available, "qty":Product.qty, "price_model":Product.price_model, "internal_code":Product.internal_code, "unit":p_unit_id, "unit_name":p_unit_name,
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











#End
