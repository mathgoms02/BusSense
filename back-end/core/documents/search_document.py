from mongoengine import Document, StringField, IntField, BooleanField

class Search(Document):
    id_cidade_origem = IntField(required=True)
    id_cidade_destino = IntField(required=True)
    id_cid = IntField(required=True)
    id_linha = StringField(max_length=255)
    sucedida = BooleanField(required=True)
    data_viagem = StringField(max_length=255)
    hora_viagem = StringField(max_length=255)
    data_criacao = StringField(max_length=255)

    meta = {'collection': 'searches'}
