from django.urls import path
from .views import ( Products, ProductItem, Shops, ShopItem, Categories,
                     CategoryItem, Attrs, Brands, AttrsItem, Search, ProductImg,
                     ShopProducts, ShopProductsItem, MainCat, Attributes,
                     ShopProductsDelete, MultiShopProductsAdd, Color, SimilarProducts,
                     Unit )


urlpatterns = [
  path('shops', Shops.as_view(), name='shops'),
  path('shop/<int:id>', ShopItem.as_view(), name='shop_item'),
  path('products', Products.as_view(), name='products'),
  path('product/<int:id>', ProductItem.as_view(), name='product_item'),
  path('productimg', ProductImg.as_view(), name='product_img'),
  path('brands', Brands.as_view(), name='brands'),
  path('maincat', MainCat.as_view(), name='MainCat'),
  path('categories', Categories.as_view(), name='categories'),
  path('category/<int:id>', CategoryItem.as_view(), name='category_item'),
  path('attr', Attributes.as_view(), name='attr'),
  path('attributes', Attrs.as_view(), name='attributes'),
  path('attribute/<int:id>', AttrsItem.as_view(), name='attribute_item'),
  path('search', Search.as_view(), name='search'),
  path('shop_products', ShopProducts.as_view(), name='shop_products'),
  path('shop_product/<int:id>', ShopProductsItem.as_view(), name='shop_product'),
  path('similar_products/<int:id>', SimilarProducts.as_view(), name='similar_products'),
  path('shop_products_delete', ShopProductsDelete.as_view(), name='shop_products_delete'),
  path('multi_add_products', MultiShopProductsAdd.as_view(), name='multi_add_products'),
  path('color', Color.as_view(), name='color'),
  path('units', Unit.as_view(), name='units'),
]
