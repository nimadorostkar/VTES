# Generated by Django 3.0.3 on 2022-07-19 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20220716_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pay_way',
            field=models.CharField(choices=[('online', 'آنلاین'), ('credit', 'اعتباری'), ('inperson', 'حضوری')], default='online', max_length=50, verbose_name='نحوه پرداخت'),
        ),
    ]