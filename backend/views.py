from django.shortcuts import render

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import EventSerializer
from rest_framework.viewsets import ModelViewSet

from .models import Event

# Create your views here.

class EventViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Events.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()
