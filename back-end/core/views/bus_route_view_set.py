from rest_framework import viewsets
from core.documents import BusRoute
from core.serializers import BusRouteSerializer

class BusRouteViewSet(viewsets.ModelViewSet):
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer
