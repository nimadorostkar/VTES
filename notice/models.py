from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django_jalali.db import models as jmodels
from authentication.models import User
from shop.models import Shop, Product, Category , ProductAttr, ProductImgs, ShopProducts, Attributes, ProductColor, Unit
from partners.models import ExchangePartner
from cart.models import Order











#------------------------------------------------------------------------------
class PartnerExchangeNotice(models.Model):
    STATUS = (
        ('answered', 'answered'),
        ('unanswered', 'unanswered'),
        ('unanswerable', 'unanswerable'),
    )
    TYPE = (
        ('cooperation-request', 'cooperation-request'),
        ('cooperation-request-answer', 'cooperation-request-answer'),
        ('exchange-request', 'exchange-request'),
        ('exchange-request-answer', 'exchange-request-answer'),
        ('buyer_response', 'buyer_response'),
        ('debtor-reposnse-accounting', 'debtor-reposnse-accounting'),
        ('creditor-alert-accounting', 'creditor-alert-accounting'),
        ('creditor-answer-accounting', 'creditor-answer-accounting'),
    )
    ANS_STATUS = (
        ('accepted', 'accepted'),
        ('declined', 'declined'),
        ('changed-value', 'changed-value'),
    )


    exchange_partner = models.ForeignKey(ExchangePartner, on_delete=models.CASCADE, verbose_name = "همکاری")
    status = models.CharField(max_length=50, choices=STATUS, verbose_name='وضعیت')
    type = models.CharField(max_length=256, choices=TYPE, verbose_name='نوع')
    shop_product = models.ForeignKey(ShopProducts, on_delete=models.CASCADE, null=True, blank=True, verbose_name = "محصول")
    quantity = models.IntegerField(null=True, blank=True, verbose_name = "تعداد")
    offer_price = models.CharField(max_length=256, null=True, blank=True, verbose_name="قیمت پیشنهادی")
    date_contract = models.CharField(max_length=256, null=True, blank=True, verbose_name = "تاریخ قرارداد")
    accountingId = models.CharField(max_length=256, null=True, blank=True, verbose_name="شناسه حسابداری")
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")
    deposit_slip_image = models.ImageField(upload_to='PartnerExchangeNotice', null=True, blank=True , verbose_name = "تصویر فیش واریزی")
    answer_status = models.CharField(max_length=70, choices=ANS_STATUS, null=True, blank=True, verbose_name='وضعیت پاسخ')

    def __str__(self):
        return str(self.status) + "|" + str(self.type)

    class Meta:
        verbose_name = "اعلان همکاری فروش"
        verbose_name_plural = "اعلانات همکاری فروش"









#-------------------------------------------------------------------------------
class ReturnedMoney(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name = "سفارش")
    amount = models.IntegerField(default=0, verbose_name='مبلغ')

    def __str__(self):
        return str(self.order) + "|" + str(self.amount)

    class Meta:
        verbose_name = "پول برگشت داده"
        verbose_name_plural = "پول های برگشتی"







#End
