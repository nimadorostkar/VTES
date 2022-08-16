from django.urls import path
from . import views


urlpatterns = [
  #path('partner_notice', views.PartnerNotice.as_view(), name='partner_notice'),
  path('cooperation_request', views.CooperationReq.as_view(), name='cooperation_request'),
  path('cooperation_req/<int:id>', views.CooperationReqItem.as_view(), name='cooperation_req'),

]
