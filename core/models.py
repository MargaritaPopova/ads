from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField


class UserProfile(models.Model):
    home_address = models.CharField(max_length=120, null=True, default='', blank=True)
    phone_number = PhoneField(blank=False, help_text='Contact phone number')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    birthdate = models.DateField(null=True, verbose_name='Date of birth', blank=True)
