from django.urls import path
from shop import views
from .views import shops,


urlpatterns = [
    #path('shops', shops.as_view(), name='shops'),
    #path('shops_detail/<int:id>/',views.shops_detail,name='shops_detail'),
]
