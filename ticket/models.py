from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django_jalali.db import models as jmodels
from authentication.models import User










#------------------------------------------------------------------------------
class Ticket(models.Model):
    STATUS = (
        ('New', 'جدید'),
        ('Accepted', 'تایید'),
        ('Pending', 'در حال بررسی'),
        ('Canceled', 'لغو شده'),
        ('Completed', 'به اتمام رسیده'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name = "کاربر")
    subject = models.CharField(max_length=256, null=True, blank=True, verbose_name="موضوع")
    type = models.CharField(max_length=256, null=True, blank=True, verbose_name="نوع")
    description = models.TextField(verbose_name="توضیحات")
    created_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ ایجاد")
    status = models.CharField(max_length=40, choices=STATUS, default='New', verbose_name='وضعیت')
    state = models.BooleanField(default=False, verbose_name='وضعیت پاسخ')
    admin_ans = models.TextField(verbose_name="پاسخ ادمین", null=True, blank=True)



    def __str__(self):
        return str(self.subject) + "|" + str(self.user)

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"
