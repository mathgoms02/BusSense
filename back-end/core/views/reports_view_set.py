from rest_framework import viewsets
from core.documents import Reports
from core.serializers import ReportsSerializer

class ReportsViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
