from rest_framework import serializers
from analytics.models import Event

class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ['name', 'additional_data']
