from rest_framework import serializers
from emtu_api.core.models import Search

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'
