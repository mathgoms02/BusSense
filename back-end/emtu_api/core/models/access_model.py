from django.db import models

class Access(models.Model):
    ip = models.CharField(max_length=255)
    data_acesso = models.CharField(max_length=255)

    class Meta:
        db_table = 'access'
