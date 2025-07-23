from rest_framework import viewsets
from core.documents import Cid
from core.serializers import CidSerializer

class CidViewSet(viewsets.ModelViewSet):
    queryset = Cid.objects.all()
    serializer_class = CidSerializer
