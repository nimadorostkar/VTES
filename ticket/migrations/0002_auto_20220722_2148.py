# Generated by Django 3.0.3 on 2022-07-22 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='type',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='نوع'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='subject',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='موضوع'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]