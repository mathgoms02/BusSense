from mongoengine import Document, StringField, IntField

class Group(Document):
    id = IntField(unique=True)
    name = StringField(max_length=255, required=True)
    description = StringField()

    meta = {'collection': 'group'}
