from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('<int:user_id>', views.ProfileView.as_view(), name='profile'),
    path('<int:user_id>/edit', views.ProfileUpdateView.as_view(), name='profile_update'),
]
