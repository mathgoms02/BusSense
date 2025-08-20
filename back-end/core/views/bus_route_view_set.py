from rest_framework_mongoengine import viewsets
from core.documents.bus_route_document import BusRoute
from core.serializers.bus_route_serializers import BusRouteSerializer

class BusRouteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint que permite a visualização das rotas de ônibus.
    
    Fornece as ações `list` (para todas as rotas) e `retrieve` (para uma rota específica pelo seu 'codigo').
    """
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer
    lookup_field = 'codigo'
