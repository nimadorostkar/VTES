# Generated by Django 3.0.3 on 2022-08-01 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangePartner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('تایید شده', 'تایید شده'), ('در انتظار تایید', 'در انتظار تایید'), ('رد شده', 'رد شده')], max_length=256, verbose_name='وضعیت')),
                ('partner_shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partner_shop', to='shop.Shop', verbose_name='فروشگاه همکار')),
                ('user_shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop', verbose_name='فروشگاه کاربر')),
            ],
            options={
                'verbose_name': 'همکار',
                'verbose_name_plural': 'همکاران',
            },
        ),
    ]
