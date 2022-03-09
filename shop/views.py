from django.shortcuts import render, get_object_or_404
from .serializers import ShopSerializer, ProductSerializer, CategorySerializer, AttributesSerializer
from rest_framework import viewsets, filters, status, pagination, mixins
from .models import Shop, Product, Category , Attributes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView








class AttributesView(viewsets.ModelViewSet):
    serializer_class = AttributesSerializer
    queryset = Attributes.objects.all()



class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()



# ------------------------------------------------------- Category ------------

class Categories(GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent',]
    search_fields = ['name', 'parent']
    ordering_fields = ['id',]

    def get(self, request, format=None):
        queryset = Category.objects.all()
        query = self.filter_queryset(Category.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CategorySerializer(query, many=True)
        return Response(serializer.data)

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
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'category']
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
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopItem(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = ShopSerializer

    def get(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, id=self.kwargs["id"])
        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, id=self.kwargs["id"])
        serializer = ShopSerializer(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, id=self.kwargs["id"])
        shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)











# ------------------------------------------------------- Products ------------

class Products(GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['provider_shop', 'category', 'approved', 'available', 'brand']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['id', 'price', 'qty', 'date_created']

    def get(self, request, format=None):
        queryset = Product.objects.all()
        query = self.filter_queryset(Product.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProductSerializer(query, many=True)
        return Response(serializer.data)

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
        return Response(serializer.data)

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
















# End
