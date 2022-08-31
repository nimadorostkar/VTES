# Generated by Django 3.0.3 on 2022-08-31 13:04

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_brand_image'),
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeReq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='تعداد')),
                ('price', models.CharField(blank=True, max_length=256, null=True, verbose_name='قیمت')),
                ('date_contract', django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='تاریخ')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to='shop.Shop', verbose_name='خریدار')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='shop.Shop', verbose_name='فروشنده')),
                ('shop_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.ShopProducts', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'درخواست مبادله',
                'verbose_name_plural': 'درخواست های مبادله',
            },
        ),
    ]
