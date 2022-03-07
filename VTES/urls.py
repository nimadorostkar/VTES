from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from shop import views
from authentication import views as auth_views



router = routers.DefaultRouter()
router.register(r'shop', views.ShopView, 'shop')
#router.register(r'product', views.ProductView, 'product')
router.register(r'category', views.CategoryView, 'category')
router.register(r'product_attr', views.Product_AttrView, 'product_attr')
router.register(r'attributes', views.AttributesView, 'attributes')
router.register(r'users', auth_views.usersView, 'users')
router.register(r'profile', auth_views.ProfileAPI, 'profile')




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/shops/', include('shop.urls')),
    path('api/login/', include(("authentication.urls", 'authentication'), namespace='authentication')),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
