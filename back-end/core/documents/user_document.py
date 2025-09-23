from django.contrib.auth.hashers import make_password, check_password

from mongoengine import Document, StringField, EmailField, IntField, ListField, ReferenceField, BooleanField

class User(Document):
    name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)    
    is_visually_impaired = BooleanField(default=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    meta = {
        'collection': 'users'
    }