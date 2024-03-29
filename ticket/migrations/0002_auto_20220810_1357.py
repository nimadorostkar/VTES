# Generated by Django 3.0.3 on 2022-08-10 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='admin_ans',
            field=models.TextField(blank=True, null=True, verbose_name='پاسخ ادمین'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='state',
            field=models.BooleanField(default=False, verbose_name='وضعیت پاسخ'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('New', 'جدید'), ('Accepted', 'تایید'), ('Pending', 'در حال بررسی'), ('Canceled', 'لغو شده'), ('Completed', 'به اتمام رسیده')], default='New', max_length=40, verbose_name='وضعیت'),
        ),
    ]
