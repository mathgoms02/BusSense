from rest_framework import viewsets
from core.documents import Group
from core.serializers import GroupSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
