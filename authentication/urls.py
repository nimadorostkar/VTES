from django.urls import path
from .views import MyUserView, verifyView, Users, Profile


urlpatterns = [
    path('login', MyUserView.as_view(), name='login'),
    path('verify', verifyView.as_view(), name='verify'),
    path('users', Users.as_view(), name='users'),
    path('profile', Profile.as_view(), name='profile'),
]
