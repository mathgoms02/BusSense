from django.db import models

class Vehicle(models.Model):
    prefix = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=255)

    class Meta:
        db_table = 'vehicles'