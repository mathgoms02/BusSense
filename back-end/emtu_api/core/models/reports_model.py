from django.db import models

class Reports(models.Model):
    email = models.EmailField()
    id_cidade_origem = models.IntegerField()
    id_cidade_destino = models.IntegerField()
    id_cid = models.IntegerField()
    data_criacao = models.CharField(max_length=255)

    class Meta:
        db_table = 'reports'
