from mongoengine import Document, StringField, IntField

class BusRoute(Document):
    id = IntField(unique=True)
    route_short_name = StringField(max_length=255, required=True)
    route_name_start = StringField(max_length=255, required=True)
    route_name_end = StringField(max_length=255, required=True)
    route_type = IntField(required=True)

    meta = {'collection': 'bus_routes'}
