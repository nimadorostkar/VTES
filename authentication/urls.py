from django.urls import path
from .views import Login, Verify, Users, Profile


urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('verify', Verify.as_view(), name='verify'),
    path('users', Users.as_view(), name='users'),
    path('profile', Profile.as_view(), name='profile'),
]
