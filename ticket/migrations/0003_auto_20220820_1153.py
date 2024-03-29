# Generated by Django 3.0.3 on 2022-08-20 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20220810_1357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='subject',
            new_name='title',
        ),
        migrations.AddField(
            model_name='ticket',
            name='answer_status',
            field=models.CharField(choices=[('New', 'جدید'), ('Accepted', 'تایید'), ('Pending', 'در حال بررسی'), ('Canceled', 'لغو شده'), ('Completed', 'به اتمام رسیده')], default=1, max_length=50, verbose_name='وضعیت'),
            preserve_default=False,
        ),
    ]
