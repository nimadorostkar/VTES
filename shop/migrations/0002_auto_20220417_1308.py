# Generated by Django 3.0.3 on 2022-04-17 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='irancode',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ایران کد'),
        ),
        migrations.AddField(
            model_name='shopproducts',
            name='internal_code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='کد داخلی محصول'),
        ),
        migrations.AddField(
            model_name='shopproducts',
            name='medium_volume_price',
            field=models.IntegerField(default=0, verbose_name='قیمت فروش با حجم متوسط'),
        ),
        migrations.AddField(
            model_name='shopproducts',
            name='min_medium_num',
            field=models.IntegerField(default=0, verbose_name='حداقل تعداد فروش با حجم متوسط'),
        ),
        migrations.AddField(
            model_name='shopproducts',
            name='min_wholesale_num',
            field=models.IntegerField(default=0, verbose_name='حداقل تعداد عمده فروشی'),
        ),
        migrations.AddField(
            model_name='shopproducts',
            name='qty',
            field=models.IntegerField(default=0, verbose_name='تعداد'),
        ),
        migrations.AddField(
            model_name='shopproducts',
            name='retail_price',
            field=models.IntegerField(default=0, verbose_name='قیمت خرده فروشی'),
        ),
        migrations.AddField(
            model_name='shopproducts',
            name='wholesale_price',
            field=models.IntegerField(default=0, verbose_name='قیمت عمده فروشی'),
        ),
    ]
