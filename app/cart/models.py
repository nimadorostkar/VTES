from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from authentication.models import User
from shop.models import ShopProducts









#------------------------------------------------------------------------------
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address', verbose_name = "کاربر")
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











#------------------------------------------------------------------------------
class ShippingTime(models.Model):
    date = models.DateField(verbose_name = "تاریخ")
    CHOICES = ( ('۹ تا ۱۲','۹ تا ۱۲'), ('۱۲ تا ۱۵','۱۲ تا ۱۵'), ('۱۵ تا ۱۸','۱۵ تا ۱۸'), ('۱۸ تا ۲۱','۱۸ تا ۲۱') )
    time = models.CharField(max_length=256, choices=CHOICES, verbose_name = "ساعت")


    def __str__(self):
        return str(self.date) + str(self.time)

    class Meta:
        verbose_name = "زمان ارسال"
        verbose_name_plural = "زمان ارسال"










#------------------------------------------------------------------------------
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_user', verbose_name = "کاربر")
    products = models.ManyToManyField(ShopProducts, verbose_name = "محصولات")


    def __str__(self):
        return str(self.user) + str(self.products)

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد های خرید"














#End
