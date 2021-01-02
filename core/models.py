from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField


class UserProfile(models.Model):
    home_address = models.CharField(max_length=120, null=True, default='')
    phone_number = PhoneField(blank=True, help_text='Contact phone number')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)
    birthdate = models.DateField(null=True, verbose_name='Date of birth', blank=True)
