# Generated by Django 3.0.3 on 2022-09-18 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '__first__'),
        ('partners', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerExchangeNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('answered', 'answered'), ('unanswered', 'unanswered'), ('unanswerable', 'unanswerable')], max_length=50, verbose_name='وضعیت')),
                ('type', models.CharField(choices=[('cooperation-request', 'cooperation-request'), ('cooperation-request-answer', 'cooperation-request-answer'), ('exchange-request', 'exchange-request'), ('exchange-request-answer', 'exchange-request-answer'), ('buyer_response', 'buyer_response'), ('debtor-reposnse-accounting', 'debtor-reposnse-accounting'), ('creditor-alert-accounting', 'creditor-alert-accounting'), ('creditor-answer-accounting', 'creditor-answer-accounting')], max_length=256, verbose_name='نوع')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='تعداد')),
                ('offer_price', models.CharField(blank=True, max_length=256, null=True, verbose_name='قیمت پیشنهادی')),
                ('date_contract', models.CharField(blank=True, max_length=256, null=True, verbose_name='تاریخ قرارداد')),
                ('accountingId', models.CharField(blank=True, max_length=256, null=True, verbose_name='شناسه حسابداری')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('deposit_slip_image', models.ImageField(blank=True, null=True, upload_to='PartnerExchangeNotice', verbose_name='تصویر فیش واریزی')),
                ('answer_status', models.CharField(choices=[('accepted', 'accepted'), ('declined', 'declined'), ('changed-value', 'changed-value')], max_length=70, verbose_name='وضعیت پاسخ')),
                ('exchange_partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partners.ExchangePartner', verbose_name='همکاری')),
                ('shop_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.ShopProducts', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'اعلان همکاری فروش',
                'verbose_name_plural': 'اعلانات همکاری فروش',
            },
        ),
    ]
