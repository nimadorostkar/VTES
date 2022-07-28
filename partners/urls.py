from django.urls import path
from .views import Partners, PartnerItem


urlpatterns = [
  path('partners', Partners.as_view(), name='partners'),
  path('partner/<int:id>', PartnerItem.as_view(), name='partner'),
]
