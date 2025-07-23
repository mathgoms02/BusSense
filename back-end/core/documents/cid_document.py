from mongoengine import Document, StringField, IntField

class Cid(Document):
    id = IntField(unique=True)
    cod = StringField(max_length=255)
    diagnostic = StringField()
    observations = StringField()
    companion = StringField()
    duration = IntField()
    requirements = StringField()
    group = StringField()
    slugdiagnostic = StringField()

    meta = {'collection': 'cids'}
