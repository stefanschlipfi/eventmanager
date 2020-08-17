from rest_framework import serializers
from .models import Event,EventUser

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['id']

class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        exclude = ['id']
        depth = 1