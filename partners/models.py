from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django_jalali.db import models as jmodels
from authentication.models import User
from shop.models import Shop









#------------------------------------------------------------------------------
class ExchangePartner(models.Model):
    user_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name = "فروشگاه کاربر")
    partner_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='partner_shop', verbose_name = "فروشگاه همکار")
    CHOICES = ( ('تایید شده','تایید شده'), ('در انتظار تایید','در انتظار تایید'), ('رد شده','رد شده') )
    status = models.CharField(max_length=256, choices=CHOICES, verbose_name="وضعیت")

    def __str__(self):
        return str(self.user_shop) + "|" + str(self.partner_shop) + "|" + str(self.status)

    class Meta:
        verbose_name = "همکار"
        verbose_name_plural = "همکاران"










#End
