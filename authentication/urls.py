from django.urls import path
from . import views
from .views import MyUserView, verifyView


urlpatterns = [
    path('', MyUserView.as_view(), name='MyUserView'),    # API
    path('verify', verifyView.as_view(), name='verifyView'), # API
]
