from mongoengine import Document, StringField, IntField

class Cid(Document):
    cod = StringField(max_length=255)
    diagnostic = StringField()
    observations = StringField()
    companion = StringField()
    duration = IntField()
    requirements = StringField()
    group = StringField()
    slugdiagnostic = StringField()

    meta = {'collection': 'cids'}
