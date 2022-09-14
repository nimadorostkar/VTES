from django.urls import path
from . import views




urlpatterns = [
  #
  path('cart', views.Cart.as_view(), name='cart'),
  path('add_to_cart', views.AddToCart.as_view(), name='add_to_cart'),
  path('add_to_cart/<int:id>', views.AddToCartItem.as_view(), name='add_to_cart'),
  #
  path('address', views.Address.as_view(), name='address'),
  path('address_item/<int:id>', views.AddressItem.as_view(), name='address_item'),
  #
  path('order', views.Order.as_view(), name='order'),
  path('postway', views.PostWay.as_view(), name='postway'),
]
