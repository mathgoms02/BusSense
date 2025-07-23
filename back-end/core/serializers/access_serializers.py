from rest_framework_mongoengine import serializers
from core.documents import Access

class AccessSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Access
        fields = '__all__'
