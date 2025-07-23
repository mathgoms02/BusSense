from rest_framework_mongoengine import serializers
from core.documents import Vehicle

class VehicleSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
