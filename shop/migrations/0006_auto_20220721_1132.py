# Generated by Django 3.0.3 on 2022-07-21 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20220721_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.City', verbose_name='شهر'),
        ),
    ]