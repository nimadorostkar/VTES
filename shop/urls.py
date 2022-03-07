from django.urls import path, re_path
from shop import views



urlpatterns = [
    path('products', views.Product_list, name='products'),
]
