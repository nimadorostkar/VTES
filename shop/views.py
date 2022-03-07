from django.shortcuts import render, get_object_or_404
from .serializers import ShopSerializer, ProductSerializer, CategorySerializer, Product_AttrSerializer, AttributesSerializer
from rest_framework import viewsets, filters, status, pagination, mixins
from .models import Shop, Product, Product_Attr, Category , Attributes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import GenericAPIView





class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()





class Product_AttrView(viewsets.ModelViewSet):
    serializer_class = Product_AttrSerializer
    queryset = Product_Attr.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'attribute']
    search_fields = ['attribute', 'product']



class AttributesView(viewsets.ModelViewSet):
    serializer_class = AttributesSerializer
    queryset = Attributes.objects.all()




class ShopView(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,) #https://testdriven.io/blog/built-in-permission-classes-drf/
    queryset = Shop.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'user']
    search_fields = ['name', 'phone', 'description']
    ordering_fields = ['name', 'email', 'date_created']




'''
class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()


@api_view(['GET', 'POST'])
def Product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            # create product
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Products(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''




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
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs["id"])
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# End
