from mongoengine import Document, StringField

class City(Document):
    name = StringField(max_length=255, required=True)

    meta = {'collection': 'city'}
