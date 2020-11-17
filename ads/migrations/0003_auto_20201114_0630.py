# Generated by Django 3.1.2 on 2020-11-14 06:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ads', '0002_ad_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='image',
        ),
        migrations.AddField(
            model_name='ad',
            name='content_type',
            field=models.CharField(help_text='The MIMEType of the file', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='ad',
            name='picture',
            field=models.BinaryField(editable=True, null=True),
        ),
    ]