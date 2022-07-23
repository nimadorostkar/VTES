from django.urls import path
from .views import Partners


urlpatterns = [
  path('partners', Partners.as_view(), name='partners'),
]
