from django.urls import path
from .views import Partners, PartnerItem, PartnersProducts, MultiPartners, MultiPartnersDel


urlpatterns = [
  path('partners', Partners.as_view(), name='partners'),
  path('multi_partners', MultiPartners.as_view(), name='multi_partners'),
  path('multi_partners_delete', MultiPartnersDel.as_view(), name='multi_partners_delete'),
  path('partner/<int:id>', PartnerItem.as_view(), name='partner'),
  path('partners_products', PartnersProducts.as_view(), name='partners_products'),
]
