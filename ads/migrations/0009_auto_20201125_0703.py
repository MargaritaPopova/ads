# Generated by Django 3.1.2 on 2020-11-25 07:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0008_auto_20201125_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='text',
            field=models.TextField(max_length=500, validators=[django.core.validators.MaxLengthValidator(500, 'Description must be less than 500 characters')]),
        ),
    ]
