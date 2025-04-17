from rest_framework import viewsets
from emtu_api.core.models import Group
from emtu_api.core.serializers import GroupSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
