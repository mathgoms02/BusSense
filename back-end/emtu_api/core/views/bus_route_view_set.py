from rest_framework import viewsets
from emtu_api.core.models import BusRoute
from emtu_api.core.serializers import BusRouteSerializer

class BusRouteViewSet(viewsets.ModelViewSet):
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer
