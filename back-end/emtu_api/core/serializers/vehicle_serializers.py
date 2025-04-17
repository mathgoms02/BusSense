from rest_framework import serializers
from emtu_api.core.models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
