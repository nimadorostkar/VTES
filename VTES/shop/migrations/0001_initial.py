# Generated by Django 4.0.2 on 2022-02-16 23:51

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='نام')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('mptt_level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='والد', to='shop.category')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='نام فروشگاه')),
                ('logo', models.ImageField(default='default.png', upload_to='logos', verbose_name='لوگو فروشگاه')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='شماره تماس')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, verbose_name='ایمیل')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='آدرس')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='توضیحات')),
                ('date_created', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='shop.category', verbose_name='دسته بند')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='authentication.profile', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'فروشگاه',
                'verbose_name_plural': 'فروشگاه ها',
            },
        ),
    ]
