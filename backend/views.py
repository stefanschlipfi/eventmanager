from django.shortcuts import render

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import EventSerializer,EventUserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response

from .models import Event,EventUser

# Create your views here.

class EventViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Events.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def list(self, request, **kwargs):
        return_data = []
        for event in Event.objects.all():
            resp = EventSerializer(event).data
            sermembers = []
            for member in event.get_members():
                memberser = EventUserSerializer(instance=member)
                sermembers.append(memberser.data)
            resp['members'] = sermembers
            return_data.append(resp)

        return Response(data = return_data)

class EventUserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Events.
    """
    serializer_class = EventUserSerializer
    queryset = EventUser.objects.all()

