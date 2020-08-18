from rest_framework import serializers
from .models import Event,EventUser

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = []

class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        exclude = []
        depth = 1