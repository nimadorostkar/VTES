from django.urls import path
from . import views




urlpatterns = [
  #
  path('exchanges', views.Exchanges.as_view(), name='exchanges'),
  path('exchanges/<int:id>', views.ExchangesItem.as_view(), name='exchanges_item'),
  #
  path('sales', views.Sales.as_view(), name='sales'),
  path('sales/<int:id>', views.SalesItem.as_view(), name='sales_item'),
  #
  path('purchases', views.Purchases.as_view(), name='purchases'),
  path('purchases/<int:id>', views.PurchasesItem.as_view(), name='purchases_item'),
]
