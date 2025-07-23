from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class Access(Document):
    ip = StringField(required=True, max_length=255)
    data_acesso = DateTimeField(default=datetime.astimezone)

    meta = {
        'collection': 'access'  # equivale ao db_table do Django
    }
