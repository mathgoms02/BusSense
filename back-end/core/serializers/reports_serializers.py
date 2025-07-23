from rest_framework_mongoengine import serializers
from core.documents import Reports

class ReportsSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Reports
        fields = '__all__'
