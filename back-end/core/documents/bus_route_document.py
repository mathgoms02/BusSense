from mongoengine import (
    Document,
    StringField,
    FloatField,
    ListField,
    EmbeddedDocument,
    EmbeddedDocumentField
)

# Documento aninhado para representar cada ponto de parada
class BusStop(EmbeddedDocument):
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)
    endereco = StringField(max_length=255, required=True)
    raio = FloatField()
    sequencia = FloatField()
    id = FloatField(required=True)

# Documento aninhado para cada sentido da rota (ida/volta)
class RouteDirection(EmbeddedDocument):
    sentido = StringField(max_length=10, required=True)
    destino = StringField(max_length=255, required=True)
    tempo = FloatField()
    horarios = ListField(StringField(max_length=10))
    pontos = ListField(EmbeddedDocumentField(BusStop))

# Documento principal para a rota de ônibus
class BusRoute(Document):
    codigo = StringField(primary_key=True, max_length=50)
    tarifa = FloatField()
    rotas = ListField(EmbeddedDocumentField(RouteDirection))

    meta = {'collection': 'bus_routes'}