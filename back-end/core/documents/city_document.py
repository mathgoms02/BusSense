from mongoengine import Document, StringField, IntField

class City(Document):
    id = IntField(unique=True)
    name = StringField(max_length=255, required=True)

    meta = {'collection': 'city'}
