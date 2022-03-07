from django.urls import path
from .views import Products, ProductItem


urlpatterns = [
  path('products', Products.as_view(), name='products'),
  path('product/<int:id>', ProductItem.as_view(), name='product'),
]
