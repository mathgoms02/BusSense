from mongoengine import Document, StringField, EmailField, IntField

class Reports(Document):
    id = IntField(unique=True)
    email = EmailField(required=True)
    id_cidade_origem = IntField(required=True)
    id_cidade_destino = IntField(required=True)
    id_cid = IntField(required=True)
    data_criacao = StringField(max_length=255)

    meta = {'collection': 'reports'}
