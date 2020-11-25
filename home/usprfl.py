from django.contrib.auth.models import User
from .models import UserProfile

u = User.objects.get(username='user3')
print(u.__dict__)