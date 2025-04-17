from rest_framework import viewsets
from emtu_api.core.models import User
from emtu_api.core.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
