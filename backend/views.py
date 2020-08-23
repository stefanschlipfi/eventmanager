from django.shortcuts import render

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import EventSerializer,EventUserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework import status
from .models import Event,EventUser

from django.db import DataError
from .exceptions import BadRequestException,ObjectExistsException
# Create your views here.

class EventMixin():
    def get_event_list(self):
        return_data = []
        for event in Event.objects.all():
            resp = EventSerializer(event).data
            sermembers = []
            for member in event.get_members():
                memberser = EventUserSerializer(instance=member)
                sermembers.append(memberser.data)
            resp['members'] = sermembers
            return_data.append(resp)
        return return_data

class EventViewSet(EventMixin,ModelViewSet):
    """
    A viewset for viewing and editing Events.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def list(self, request, **kwargs):
        return Response(data = self.get_event_list())

class EventUserViewSet(EventMixin,ModelViewSet):
    """
    A viewset for viewing and editing Events.
    """
    serializer_class = EventUserSerializer
    queryset = EventUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user = get_object_or_404(User,pk=data['user_id'])
            event = get_object_or_404(Event,pk=data['event_id'])
            try:
                new_eventuser_obj = EventUser.objects.create(event=event,user=user,action=data['action'])
            except DataError as e:
                raise ObjectExistsException(detail=e) 
            else:
                return Response(data={"created":data,'event_list':self.get_event_list()},status=status.HTTP_201_CREATED)
        else:
            #raise Serializer Exception
            super().create(request, *args, **kwargs)


