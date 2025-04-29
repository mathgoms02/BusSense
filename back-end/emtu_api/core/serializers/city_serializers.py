from rest_framework import serializers
from emtu_api.core.models import City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
