from rest_framework_mongoengine import serializers
from core.documents.bus_route_document import BusRoute, RouteDirection, BusStop

class BusStopSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = BusStop
        fields = '__all__'

class RouteDirectionSerializer(serializers.EmbeddedDocumentSerializer):
    pontos = BusStopSerializer(many=True)

    class Meta:
        model = RouteDirection
        fields = '__all__'

class BusRouteSerializer(serializers.DocumentSerializer):
    rotas = RouteDirectionSerializer(many=True)

    class Meta:
        model = BusRoute
        depth = 2 # Garante que os documentos aninhados (pontos dentro de rotas) sejam incluídos
        fields = '__all__'