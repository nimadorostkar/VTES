from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from authentication.models import User
from shop.models import ShopProducts
from shortuuid.django_fields import ShortUUIDField







#------------------------------------------------------------------------------
class PostWay(models.Model):
    way = models.CharField(max_length=60, verbose_name='روش سفارش')
    price = models.IntegerField(verbose_name='هزینه ارسال')

    class Meta:
        verbose_name = 'روش‌‌ ارسال'
        verbose_name_plural = 'روش‌های ارسال'

    def __str__(self):
        return self.way









#------------------------------------------------------------------------------
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address', verbose_name = "کاربر")
    CHOICES = ( ('خانه','خانه'), ('فروشگاه','فروشگاه'), ('انبار','انبار'))
    place = models.CharField(max_length=256, null=True, blank=True, choices=CHOICES, verbose_name = "محل")
    address = models.CharField(max_length=256, verbose_name = "آدرس")
    phone_number = models.CharField(max_length=256, verbose_name = "شماره تماس")
    postal_code = models.CharField(max_length=256, verbose_name = "کد پستی")
    name = models.CharField(max_length=256, verbose_name = "نام تحویل گیرنده")
    lname = models.CharField(max_length=256, verbose_name = "نام خانوادگی تحویل گیرنده")
    lat_long = models.CharField(max_length=256, null=True, blank=True, verbose_name = "lat & long")

    def __str__(self):
        return str(self.user) + str(self.place)

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"











#------------------------------------------------------------------------------
class ShippingTime(models.Model):
    date = models.CharField(max_length=256, verbose_name = "تاریخ")
    CHOICES = ( ('۹ تا ۱۲','۹ تا ۱۲'), ('۱۲ تا ۱۵','۱۲ تا ۱۵'), ('۱۵ تا ۱۸','۱۵ تا ۱۸'), ('۱۸ تا ۲۱','۱۸ تا ۲۱') )
    time = models.CharField(max_length=256, choices=CHOICES, verbose_name = "ساعت")


    def __str__(self):
        return str(self.date) + str(self.time)

    class Meta:
        verbose_name = "زمان ارسال"
        verbose_name_plural = "زمان ارسال"











#------------------------------------------------------------------------------
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(ShopProducts, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return self.product.product.name

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'













#------------------------------------------------------------------------------
class Order(models.Model):
    STATUS = (
        ('New', 'جدید'),
        ('Accepted', 'تایید سفارش'),
        ('Preparing', 'آماده سازی سفارش'),
        ('InPostOffice', 'تحویل به پست'),
        ('Arrive', 'تحویل به مشتری'),
        ('Canceled', 'لغو شده'),
    )
    PAY_WAY = ( ('online', 'آنلاین'), ('credit', 'اعتباری'), ('inperson', 'حضوری'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    #code = models.CharField(max_length=10, editable=False, verbose_name='کد سفارش')
    code = ShortUUIDField(length=8, max_length=15, alphabet="abcdefg1234", editable=False)
    carts = models.ManyToManyField(Cart, verbose_name='سبد محصولات')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='آدرس')
    delivery_time = models.ForeignKey(ShippingTime, on_delete=models.CASCADE, verbose_name='زمان تحویل')
    post_way = models.ForeignKey(PostWay, on_delete=models.CASCADE, verbose_name='نحوه ارسال')
    pay_way = models.CharField(max_length=50, choices=PAY_WAY, default='online', verbose_name='نحوه پرداخت')
    total = models.IntegerField(verbose_name='جمع مبلغ کل سفارشات')
    amount = models.IntegerField(verbose_name='جمع تعداد کل سفارشات')
    status = models.CharField(max_length=30, choices=STATUS, default='New', verbose_name='وضعیت')
    admin_note = models.CharField(blank=True, max_length=100, verbose_name='یادداشت ادمین')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')
    update_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'



















#End
