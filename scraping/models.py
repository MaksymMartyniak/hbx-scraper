from django.db import models
from django.contrib.auth.models import User


class Clothing(models.Model):
    sku = models.CharField(max_length=100, default=None)
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    url = models.URLField(default=None)
    img = models.URLField(default=None)


class Category(models.Model):
    MEN = 'M'
    WOMEN = 'W'

    GENDER = [
        (MEN, 'Men'),
        (WOMEN, 'Women'),
    ]

    title = models.CharField(max_length=200)
    gender = models.CharField(max_length=3, choices=GENDER, default=MEN)
    code = models.CharField(max_length=200, default=None)
    url = models.URLField()
