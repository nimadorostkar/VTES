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
    ANSWER_STATUS = (
        ('accepted', 'accepted'),
        ('declined', 'declined'),
        ('not-declinable', 'not-declinable'),
    )
    TYPE = ( 
        ('suggestion', 'suggestion'),
        ('support', 'support'),
        ('add-attributes', 'add-attributes'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name = "کاربر")
    title = models.CharField(max_length=256, null=True, blank=True, verbose_name="موضوع")
    type = models.CharField(max_length=200, choices=TYPE, default='suggestion', verbose_name="نوع")
    status = models.CharField(max_length=200, choices=STATUS, default='New', verbose_name='وضعیت')
    answer_status = models.CharField(max_length=200, choices=ANSWER_STATUS, default='not-declinable', verbose_name='وضعیت پاسخ')
    description = models.TextField(verbose_name="توضیحات")
    state = models.BooleanField(default=False, verbose_name='وضعیت پاسخ')
    admin_ans = models.TextField(verbose_name="پاسخ ادمین", null=True, blank=True)
    created_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ ایجاد")

    def __str__(self):
        return str(self.title) + "|" + str(self.user)

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"
