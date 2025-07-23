from mongoengine import Document, StringField

class Vehicle(Document):
    prefix = StringField(max_length=255)
    name = StringField(max_length=255)
    group = StringField(max_length=255)

    meta = {'collection': 'vehicles'}
