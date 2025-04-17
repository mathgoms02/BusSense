from rest_framework import viewsets
from emtu_api.core.models import Access
from emtu_api.core.serializers import AccessSerializer

class AccessViewSet(viewsets.ModelViewSet):
    queryset = Access.objects.all()
    serializer_class = AccessSerializer
