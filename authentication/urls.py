from django.urls import path
from . import views
from .views import MyUserView, verifyView


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('otp', MyUserView.as_view(), name='MyUserView'),    # API
    path('verify', verifyView.as_view(), name='verifyView'), # API
]
