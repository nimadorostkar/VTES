from django.urls import path
from .views import Products, ProductItem, Shops, ShopItem


urlpatterns = [
  path('products', Products.as_view(), name='products'),
  path('product/<int:id>', ProductItem.as_view(), name='product_item'),
  path('shops', Shops.as_view(), name='shops'),
  path('shop/<int:id>', ShopItem.as_view(), name='shop_item'),
]
