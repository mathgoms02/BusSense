from rest_framework import viewsets
from emtu_api.core.models import Vehicle
from emtu_api.core.serializers import VehicleSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
