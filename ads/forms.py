from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

from ads.humanize import naturalsize
from ads.models import Ad


class CreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)
    picture = forms.FileField(required=False, label='File to Upload <= ' + max_upload_limit_text)
    upload_field_name = 'picture'

    class Meta:
        model = Ad
        fields = ['title', 'text', 'price', 'picture']

    def clean(self):
        """
        Validates the size of the picture
        :return: None
        """
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', "File must be < " + self.max_upload_limit_text + " bytes")

    def save(self, commit=True):
        """
        Converts uploaded File object to a picture
        :param commit: determines whether the record is committed to database
        :return: object instance
        """
        instance = super(CreateForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture  # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance


class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
