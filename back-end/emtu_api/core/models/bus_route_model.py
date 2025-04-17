from django.db import models

class BusRoute(models.Model):
    route_short_name = models.CharField(max_length=255)
    route_name_start = models.CharField(max_length=255)
    route_name_end = models.CharField(max_length=255)
    route_type = models.IntegerField()

    class Meta:
        db_table = 'bus_routes'
