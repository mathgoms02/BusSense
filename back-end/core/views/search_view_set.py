from rest_framework import viewsets
from core.documents import Search
from core.serializers import SearchSerializer

class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
