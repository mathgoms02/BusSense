from rest_framework import serializers
from emtu_api.core.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
