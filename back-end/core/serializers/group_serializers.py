from rest_framework_mongoengine import serializers
from core.documents import Group

class GroupSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Group
        fields = '__all__'
