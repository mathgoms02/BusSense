from mongoengine import Document, StringField, IntField

class SequenceDocument(Document):
    # O nome do contador (ex: 'city_id', 'user_id')
    name = StringField(primary_key=True) 
    # O último valor da sequência
    sequence_value = IntField(default=0)

    meta = {
        'collection': 'sequences'
    }
