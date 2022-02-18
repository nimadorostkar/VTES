from django.shortcuts import render
from .serializers import ShopSerializer, ProductSerializer, CategorySerializer, Product_AttrSerializer, AttributesSerializer
from rest_framework import viewsets, filters
from .models import Shop, Product, Product_Attr, Category , Attributes
from django_filters.rest_framework import DjangoFilterBackend
from django.views import generic





#------------------------------------------------------------------------------
class shops(generic.ListView):
    model = Shop
    template_name = 'shop/shops.html'
    context_object_name = 'shops'
    queryset = Shop.objects.all()
    ordering = ['-date_created']
    paginate_by = 6








class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()





class Product_AttrView(viewsets.ModelViewSet):
    serializer_class = Product_AttrSerializer
    queryset = Product_Attr.objects.all()



class AttributesView(viewsets.ModelViewSet):
    serializer_class = AttributesSerializer
    queryset = Attributes.objects.all()




class ShopView(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'user']
    search_fields = ['name', 'phone', 'description']
    ordering_fields = ['name', 'email', 'date_created']





class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()











# End
