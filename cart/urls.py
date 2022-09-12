from django.urls import path
from . import views




urlpatterns = [
  path('add_to_cart', views.AddToCart.as_view(), name='add_to_cart'),
]
