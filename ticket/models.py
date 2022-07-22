from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django_jalali.db import models as jmodels
from authentication.models import User










#------------------------------------------------------------------------------
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = "کاربر")
    subject = models.CharField(max_length=256, verbose_name="موضوع")
    description = models.TextField()

    def __str__(self):
        return str(self.subject) + "|" + str(self.user)

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"