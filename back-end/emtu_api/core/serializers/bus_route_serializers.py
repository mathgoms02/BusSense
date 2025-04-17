from rest_framework import serializers
from emtu_api.core.models import BusRoute

class BusRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusRoute
        fields = '__all__'
