from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from ads.humanize import naturalsize
from core.models import UserProfile


class ProfileForm(forms.ModelForm):
    max_upload_limit = 2 * 256 * 256
    max_upload_limit_text = naturalsize(max_upload_limit)
    picture = forms.ImageField(required=False, label='File to Upload <= ' + max_upload_limit_text)
    upload_field_name = 'picture'

    class Meta:
        model = UserProfile
        labels = {
            'home_address': 'Your home address',
            'phone_number': 'Phone number',
            'birthdate': 'Date of birth',
        }
        fields = ['home_address', 'phone_number', 'birthdate', 'picture']
        widgets = {'birthdate': forms.SelectDateWidget(years=[year for year in range(1930, 2003)])}




