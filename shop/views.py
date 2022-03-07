from django.shortcuts import render
from .serializers import ShopSerializer, ProductSerializer, CategorySerializer, Product_AttrSerializer, AttributesSerializer
from rest_framework import viewsets, filters, status
from .models import Shop, Product, Product_Attr, Category , Attributes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response








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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# End
