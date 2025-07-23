from mongoengine import Document, StringField, EmailField, IntField

class User(Document):
    id = IntField(unique=True)
    name = StringField(max_length=255, required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=255, required=True)

    meta = {'collection': 'users'}
