from rest_framework import serializers
from emtu_api.core.models import Access

class AccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Access
        fields = '__all__'
