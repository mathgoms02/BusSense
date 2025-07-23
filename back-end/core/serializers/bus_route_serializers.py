from rest_framework_mongoengine import serializers
from core.documents import BusRoute

class BusRouteSerializer(serializers.DocumentSerializer):
    class Meta:
        model = BusRoute
        fields = '__all__'
