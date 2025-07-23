from rest_framework_mongoengine import serializers
from core.documents import Cid

class CidSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Cid
        fields = '__all__'
