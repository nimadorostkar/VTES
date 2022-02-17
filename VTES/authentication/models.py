from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatechars
from django_jalali.db import models as jmodels







#------------------------------------------------------------------------------
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True,related_name='profile',verbose_name = "کاربر")
  legal = models.BooleanField(default=False, verbose_name = "شخصیت حقوقی")
  phone = models.CharField(max_length=50,null=True, blank=True,verbose_name = "شماره تماس")
  company = models.CharField(max_length=80, verbose_name = "نام شرکت")
  address = models.CharField(max_length=200, null=True, blank=True, verbose_name = "آدرس")
  date_created = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ ایجاد")

  def __str__(self):
    return str(self.user)

  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
      if created:
          Profile.objects.create(user=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
      instance.profile.save()

  def get_absolute_url(self):
      return reverse('user_detail',args=[self.id])

  class Meta:
      verbose_name = "کاربر"
      verbose_name_plural = "کاربران"














#End
