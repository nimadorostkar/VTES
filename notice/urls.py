from django.urls import path
from . import views


urlpatterns = [
  #path('partner_notice', views.PartnerNotice.as_view(), name='partner_notice'),
  path('partner_req', views.PartnerReq.as_view(), name='partner_req'),
  path('partner_req_item/<int:id>', views.PartnerReqItem.as_view(), name='partner_req_item'),

]
