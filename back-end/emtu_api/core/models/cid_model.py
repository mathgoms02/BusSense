from django.db import models

class Cid(models.Model):
    cod = models.CharField(max_length=255, null=True, blank=True)
    diagnostic = models.TextField(null=True, blank=True)
    observations = models.TextField(null=True, blank=True)
    companion = models.TextField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    group = models.TextField(null=True, blank=True)
    slugdiagnostic = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'cids'
