from mongoengine import Document, StringField

class Group(Document):
    name = StringField(max_length=255, required=True)
    description = StringField()

    meta = {'collection': 'group'}
