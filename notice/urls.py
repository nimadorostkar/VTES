from django.urls import path
from . import views


urlpatterns = [
  path('partner_req_notice', views.PartnerReq.as_view(), name='partner_req_notice'),
  path('partner_req_item_notice/<int:id>', views.PartnerReqItem.as_view(), name='partner_req_item_notice'),
  #
  path('exchange_request', views.ExchangeReq.as_view(), name='exchange_request'),
  path('exchange_request_item/<int:id>', views.ExchangeReqItem.as_view(), name='exchange_request_item'),
  #
  path('ticket_notice', views.TicketNotice.as_view(), name='ticket_notice'),

]
