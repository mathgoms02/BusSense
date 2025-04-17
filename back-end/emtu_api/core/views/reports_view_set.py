from rest_framework import viewsets
from emtu_api.core.models import Reports
from emtu_api.core.serializers import ReportsSerializer

class ReportsViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
