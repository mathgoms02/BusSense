from django.db import models

class Search(models.Model):
    id_cidade_origem = models.IntegerField()
    id_cidade_destino = models.IntegerField()
    id_cid = models.IntegerField()
    id_linha = models.CharField(max_length=255, null=True, blank=True)
    sucedida = models.BooleanField()
    data_viagem = models.CharField(max_length=255)
    hora_viagem = models.CharField(max_length=255)
    data_criacao = models.CharField(max_length=255)

    class Meta:
        db_table = 'searches'
