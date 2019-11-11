import uuid

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import models
from django.template import loader
from django_jalali.db import models as jmodels


class Profile(models.Model):
    objects = jmodels.jManager()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = jmodels.jDateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
