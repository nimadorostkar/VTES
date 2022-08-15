# Generated by Django 3.0.3 on 2022-08-15 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0001_initial'),
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partnerexchangenotice',
            name='partner_shop',
        ),
        migrations.RemoveField(
            model_name='partnerexchangenotice',
            name='user_shop',
        ),
        migrations.AddField(
            model_name='partnerexchangenotice',
            name='exchange_partner',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='partners.ExchangePartner', verbose_name='همکاری'),
            preserve_default=False,
        ),
    ]
