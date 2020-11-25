from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models


class Ad(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    text = models.CharField(max_length=250,
                            validators=[MaxLengthValidator(250, 'Description must be less than 250 characters')])
    fulldesc = models.TextField(default="")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      through='Comment', related_name='comments_owned')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       through='Fav', related_name='favorite_ads')

    def __str__(self):
        return self.title

    def get_likes(self):
        return Fav.objects.filter(ad=self).count()


class Comment(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 15: return self.text
        return self.text[:11] + ' ...'


class Fav(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('ad', 'user')

    def __str__(self):
        return '%s likes %s' % (self.user.username, self.ad.title[:10])



