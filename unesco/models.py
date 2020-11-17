from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class States(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class ISO(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Site(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    justification = models.TextField(null=True, default=None)
    year = models.IntegerField(null=True, default=None)
    longitude = models.FloatField()
    latitude = models.FloatField()
    area_hectares = models.FloatField(null=True, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    states = models.ForeignKey(States, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    iso = models.ForeignKey(ISO, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
