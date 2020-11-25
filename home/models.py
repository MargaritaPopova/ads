from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    home_address = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=32)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField()
