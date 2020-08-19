from rest_framework import serializers
from .models import Event,EventUser
from .validators import EventUserValidator
from django.core.validators import MinValueValidator

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = []

class EventUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True,validators=[MinValueValidator(1)])
    event_id = serializers.IntegerField(required=True,validators=[MinValueValidator(1)])
    class Meta:
        model = EventUser
        exclude = []
        depth = 1
        

    def create(self,validated_data):
        print(validated_data)
        event_user = EventUser.objects.create(
            action=validated_data['action']
        )
        return event_user