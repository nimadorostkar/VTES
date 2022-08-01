from django.urls import path
from .views import Ticket


urlpatterns = [
  path('ticket', Ticket.as_view(), name='ticket'),
]
