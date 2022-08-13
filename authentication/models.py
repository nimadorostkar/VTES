from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.myusermanager import UserManager
from django.utils.html import format_html




class User(AbstractUser):
    username = None
    mobile = models.CharField(max_length=256, unique=True, verbose_name = "شماره موبایل")
    otp = models.PositiveIntegerField(blank=True, null=True, verbose_name = "کد ورود")
    otp_create_time = models.DateTimeField(auto_now=True, verbose_name = "تاریخ ایجاد کد")
    is_legal = models.BooleanField(default=False, verbose_name = "شخصیت حقوقی")
    company = models.CharField(max_length=256, null=True, blank=True, verbose_name = "نام شرکت")
    address = models.CharField(max_length=256, null=True, blank=True, verbose_name = "آدرس")
    email_verification = models.BooleanField(default=False, verbose_name = "تایید ایمیل")
    referral_code = models.CharField(max_length=256, null=True, blank=True, verbose_name = "کد معرف")
    image = models.ImageField(default='userimg/default.png', upload_to='userimg', verbose_name = "تصویر")
    shaba_number = models.CharField(max_length=120, null=True, blank=True, verbose_name = "شماره شبا")
    card_number = models.CharField(max_length=120, null=True, blank=True, verbose_name = "شماره کارت")
    bank_account_number = models.CharField(max_length=120, null=True, blank=True, verbose_name = "شماره حساب")
    national_code = models.CharField(max_length=256, null=True, blank=True, verbose_name="کد ملی")
    postal_code = models.CharField(max_length=256, null=True, blank=True, verbose_name="کد پستی")
    telephone = models.CharField(max_length=256, null=True, blank=True, verbose_name="شماره تلفن ثابت")
    warehouse_address = models.CharField(max_length=256, null=True, blank=True, verbose_name="آدرس محل انبار")
    national_id = models.CharField(max_length=256, null=True, blank=True, verbose_name="شناسه ملی")
    reg_number = models.CharField(max_length=256, null=True, blank=True, verbose_name="شماره ثبت")
    economic_code = models.CharField(max_length=256, null=True, blank=True, verbose_name="کد اقتصادی")

    def img(self):
        return format_html("<img width=30 src='{}'>".format(self.image.url))

    objects = UserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []
    backend = 'authentication.mybackend.ModelBackend'
