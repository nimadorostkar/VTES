from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from authentication.models import User








#------------------------------------------------------------------------------
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile', verbose_name = "کاربر")
    CHOICES = ( ('خانه','خانه'), ('فروشگاه','فروشگاه'))
    place = models.CharField(max_length=256, choices=CHOICES, verbose_name = "محل")
    address = models.CharField(max_length=256, verbose_name = "آدرس")
    phone_number = models.CharField(max_length=256, verbose_name = "شماره تماس")
    postal_code = models.CharField(max_length=256, verbose_name = "کد پستی")

    def __str__(self):
        return str(self.user) + str(self.place)

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"
