# Generated by Django 3.0.3 on 2022-08-21 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_shop_invoicing'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='image',
            field=models.ImageField(blank=True, default='logos/default.png', null=True, upload_to='brands', verbose_name='لوگو '),
        ),
    ]