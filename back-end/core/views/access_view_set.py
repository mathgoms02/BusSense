from rest_framework import viewsets
from core.documents import Access
from core.serializers import AccessSerializer

class AccessViewSet(viewsets.ModelViewSet):
    queryset = Access.objects.all()
    serializer_class = AccessSerializer
