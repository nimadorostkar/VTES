from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from shop import views




router = routers.DefaultRouter()
router.register(r'shop', views.ShopView, 'shop')
router.register(r'product', views.ProductView, 'product')
router.register(r'category', views.CategoryView, 'category')
router.register(r'product_attr', views.Product_AttrView, 'product_attr')
router.register(r'attributes', views.AttributesView, 'attributes')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include("authentication.urls")),
    path('', include("shop.urls")),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
