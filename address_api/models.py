from django.db import models


class ValidAddress(models.Model):
    currency = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    public_key = models.CharField(max_length=150)
