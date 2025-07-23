from mongoengine import Document, StringField, IntField

class Vehicle(Document):
    id = IntField(unique=True)
    prefix = StringField(max_length=255)
    name = StringField(max_length=255)
    group = StringField(max_length=255)

    meta = {'collection': 'vehicles'}
