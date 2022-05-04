# Generated by Django 3.0.3 on 2022-05-05 02:38

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='ویژگی')),
            ],
            options={
                'verbose_name': 'ویژگی',
                'verbose_name_plural': 'ویژگی ها',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='نام')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('mptt_level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='والد', to='shop.Category', verbose_name='والد')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(default=False, verbose_name='تایید شده')),
                ('code', models.CharField(blank=True, max_length=50, null=True, verbose_name='کد محصول')),
                ('irancode', models.CharField(blank=True, max_length=50, null=True, verbose_name='ایران کد')),
                ('name', models.CharField(max_length=80, verbose_name='نام محصول')),
                ('banner', models.ImageField(default='products/default.png', upload_to='products', verbose_name='تصویر')),
                ('brand', models.CharField(blank=True, max_length=50, null=True, verbose_name='برند محصول')),
                ('link', models.URLField(blank=True, null=True, verbose_name='لینک محصول')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='توضیحات')),
                ('datasheet', models.FileField(blank=True, max_length=254, null=True, upload_to='datasheet', verbose_name='فایل و Datasheet')),
                ('date_created', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='shop.Category', verbose_name='دسته بند')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='نام فروشگاه')),
                ('logo', models.ImageField(default='logos/default.png', upload_to='logos', verbose_name='لوگو فروشگاه')),
                ('cover', models.ImageField(default='covers/default.png', upload_to='vovers', verbose_name='کاور فروشگاه')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='شماره تماس')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, verbose_name='ایمیل')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='توضیحات')),
                ('country', models.CharField(blank=True, max_length=20, null=True, verbose_name='کشور')),
                ('city', models.CharField(blank=True, max_length=20, null=True, verbose_name='شهر')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='آدرس')),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='کد پستی')),
                ('lat_long', models.CharField(blank=True, max_length=20, null=True, verbose_name='lat & long')),
                ('shaba_number', models.CharField(blank=True, max_length=120, null=True, verbose_name='شماره شبا')),
                ('card_number', models.CharField(blank=True, max_length=120, null=True, verbose_name='شماره کارت')),
                ('bank_account_number', models.CharField(blank=True, max_length=120, null=True, verbose_name='شماره حساب')),
                ('instagram', models.CharField(blank=True, max_length=120, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=120, null=True)),
                ('whatsapp', models.CharField(blank=True, max_length=120, null=True)),
                ('telegram', models.CharField(blank=True, max_length=120, null=True)),
                ('date_created', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('category', models.ManyToManyField(related_name='shop_category', to='shop.Category', verbose_name='دسته بند')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'فروشگاه',
                'verbose_name_plural': 'فروشگاه ها',
            },
        ),
        migrations.CreateModel(
            name='ShopProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=True, verbose_name='موجود')),
                ('internal_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='کد داخلی محصول')),
                ('qty', models.IntegerField(default=0, verbose_name='تعداد')),
                ('price_model', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], max_length=254, verbose_name='مدل قیمتی')),
                ('retail_price', models.IntegerField(default=0, verbose_name='قیمت خرده فروشی')),
                ('medium_volume_price', models.IntegerField(default=0, verbose_name='قیمت فروش با حجم متوسط')),
                ('min_medium_num', models.IntegerField(default=0, verbose_name='حداقل تعداد فروش با حجم متوسط')),
                ('wholesale_price', models.IntegerField(default=0, verbose_name='قیمت عمده فروشی')),
                ('min_wholesale_num', models.IntegerField(default=0, verbose_name='حداقل تعداد عمده فروشی')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='shop.Product', verbose_name='محصول')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Shop', to='shop.Shop', verbose_name='فروشگاه')),
            ],
            options={
                'verbose_name': 'محصول فروشگاه',
                'verbose_name_plural': 'محصولات فروشگاه',
            },
        ),
        migrations.CreateModel(
            name='ProductImgs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='products', verbose_name='تصویر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productImg', to='shop.Product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'تصاویر محصول',
                'verbose_name_plural': 'تصاویر محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', colorfield.fields.ColorField(default='#BFBFBF', image_field=None, max_length=18, samples=None, verbose_name='رنگ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_color', to='shop.ShopProducts', verbose_name='محصول مربوطه')),
            ],
            options={
                'verbose_name': 'رنگ محصول',
                'verbose_name_plural': 'رنگ محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductAttr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=60, verbose_name='مقدار')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Attributes', verbose_name='ویژگی')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_attr', to='shop.ShopProducts', verbose_name='محصول مربوطه')),
            ],
            options={
                'verbose_name': 'ویژگی محصول',
                'verbose_name_plural': 'ویژگی محصولات',
            },
        ),
    ]
