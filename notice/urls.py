from django.urls import path
from . import views


urlpatterns = [
  path('partner_notice', views.PartnerNotice.as_view(), name='partner_notice'),
]
