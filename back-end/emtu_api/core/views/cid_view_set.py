from rest_framework import viewsets
from emtu_api.core.models import Cid
from emtu_api.core.serializers import CidSerializer

class CidViewSet(viewsets.ModelViewSet):
    queryset = Cid.objects.all()
    serializer_class = CidSerializer
