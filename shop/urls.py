from django.urls import path
from .views import Products, Product


urlpatterns = [
path('products/', Products.as_view(), name='products'),
path('product/<int:id>/', Product.as_view(), name='product'),
]
