# Generated by Django 3.1.2 on 2021-01-10 04:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0010_auto_20201125_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]