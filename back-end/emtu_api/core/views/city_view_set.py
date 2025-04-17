from rest_framework import viewsets
from emtu_api.core.models import City
from emtu_api.core.serializers import CitySerializer

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
