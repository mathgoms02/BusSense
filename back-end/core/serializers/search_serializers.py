from rest_framework_mongoengine import serializers
from core.documents import Search

class SearchSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Search
        fields = '__all__'
