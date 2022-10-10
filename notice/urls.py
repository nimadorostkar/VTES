from django.urls import path
from . import views


urlpatterns = [

  path('partner_notice', views.PartnerNotice.as_view(), name='partner_notice'),
  path('partner_notice_item/<int:id>', views.PartnerNoticeItem.as_view(), name='partner_notice_item'),
  path('product_exchange_req', views.ProductExchangeReq.as_view(), name='product_exchange_req'),
  #
  path('ticket_notice', views.TicketNotice.as_view(), name='ticket_notice'),
  #
  path('sales_orders', views.SalesOrders.as_view(), name='sales_orders'),

]
