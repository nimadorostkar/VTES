from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django_jalali.db import models as jmodels
from authentication.models import User
from shop.models import Shop, Product, Category , ProductAttr, ProductImgs, ShopProducts, Attributes, ProductColor, Unit
from partners.models import ExchangePartner







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
    #user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = "کاربر")
    #partner_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partner_user', verbose_name = "همکار")
    #user_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name = "فروشگاه کاربر")
    #partner_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='partnershop', verbose_name = "فروشگاه همکار")
    exchange_partner = models.ForeignKey(ExchangePartner, on_delete=models.CASCADE, verbose_name = "همکاری")
    status = models.CharField(max_length=50, choices=STATUS, verbose_name='وضعیت')
    type = models.CharField(max_length=256, choices=TYPE, verbose_name='نوع')
    shop_product = models.ForeignKey(ShopProducts, on_delete=models.CASCADE, null=True, blank=True, verbose_name = "محصول")
    quantity = models.IntegerField(null=True, blank=True, verbose_name = "تعداد")
    offer_price = models.CharField(max_length=256, null=True, blank=True, verbose_name="قیمت پیشنهادی")
    date_contract = jmodels.jDateTimeField(null=True, blank=True, verbose_name = "تاریخ قرارداد")
    accountingId = models.CharField(max_length=256, null=True, blank=True, verbose_name="شناسه حسابداری")
    description = models.TextField(verbose_name="توضیحات")
    deposit_slip_image = models.ImageField(upload_to='PartnerExchangeNotice', null=True, blank=True , verbose_name = "تصویر فیش واریزی")
    #shopId =
    #shopName =
    #ownerName =
    #product_id =
    #product_name =
    #product_brand =
    #unit_measurment =

    def __str__(self):
        return str(self.status) + "|" + str(self.type)

    class Meta:
        verbose_name = "اعلان همکاری فروش"
        verbose_name_plural = "اعلانات همکاری فروش"










#End
