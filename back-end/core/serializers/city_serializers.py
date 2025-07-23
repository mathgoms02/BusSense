from rest_framework_mongoengine import serializers
from core.documents import City

class CitySerializer(serializers.DocumentSerializer):
    class Meta:
        model = City
        fields = '__all__'
