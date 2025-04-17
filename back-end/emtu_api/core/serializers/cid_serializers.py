from rest_framework import serializers
from emtu_api.core.models import Cid

class CidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cid
        fields = '__all__'
