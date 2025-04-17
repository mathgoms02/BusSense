from rest_framework import viewsets
from emtu_api.core.models import Search
from emtu_api.core.serializers import SearchSerializer

class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
