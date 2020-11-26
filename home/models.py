from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    home_address = models.CharField(max_length=120, null=True, default='')
    phone_number = models.CharField(max_length=32, null=True, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)
