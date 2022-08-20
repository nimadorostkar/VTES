from django.urls import path
from . import views


urlpatterns = [
  path('partner_req_notice', views.PartnerReq.as_view(), name='partner_req_notice'),
  path('partner_req_item_notice/<int:id>', views.PartnerReqItem.as_view(), name='partner_req_item_notice'),
  #
  path('ticket_notice', views.TicketNotice.as_view(), name='ticket_notice'),

]
