from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django_jalali.db import models as jmodels
from authentication.models import User
from shop.models import Shop, ShopProducts









#------------------------------------------------------------------------------
class ExchangePartner(models.Model):
    user_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name = "فروشگاه کاربر")
    partner_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='partner_shop', verbose_name = "فروشگاه همکار")
    CHOICES = ( ('تایید شده','تایید شده'), ('در انتظار تایید','در انتظار تایید'), ('رد شده','رد شده') )
    status = models.CharField(max_length=256, choices=CHOICES, verbose_name="وضعیت")

    def __str__(self):
        return str(self.user_shop) + "|" + str(self.partner_shop) + "|" + str(self.status)

    def partnerShopName(self):
        return str(self.partner_shop.name)

    def partnerShopAddress(self):
        return str(self.partner_shop.address)

    def partnerShopProvince(self):
        return str(self.partner_shop.province)

    def partnerShopCity(self):
        return str(self.partner_shop.city)

    def partner_name(self):
        return str(self.partner_shop.user.first_name) +' '+ str(self.partner_shop.user.last_name)

    def partnerShopUser(self):
        return str(self.partner_shop.user)

    def partnerShopPhone(self):
        return str(self.partner_shop.phone)

    class Meta:
        verbose_name = "همکار"
        verbose_name_plural = "همکاران"










#------------------------------------------------------------------------------
class ExchangeReq(models.Model):
    buyer = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='buyer', verbose_name = "خریدار")
    seller = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='seller', verbose_name = "فروشنده")
    shop_product = models.ForeignKey(ShopProducts, on_delete=models.CASCADE, null=True, blank=True, verbose_name = "محصول")
    quantity = models.IntegerField(null=True, blank=True, verbose_name = "تعداد")
    price = models.CharField(max_length=256, null=True, blank=True, verbose_name="قیمت")
    date_contract = jmodels.jDateTimeField(null=True, blank=True, verbose_name = "تاریخ")
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")

    def __str__(self):
        return str(self.buyer) + "|" + str(self.seller) + "|" + str(self.shop_product)

    class Meta:
        verbose_name = "درخواست مبادله"
        verbose_name_plural = "درخواست های مبادله"






















#End
