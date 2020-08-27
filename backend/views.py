from django.shortcuts import render

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import EventSerializer,EventUserSerializer,EventUserCreateSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework import status
from .models import Event,EventUser

from django.db import DataError
from .exceptions import BadRequestException,ObjectExistsException
from rest_framework.exceptions import PermissionDenied,NotFound
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
    
    def retrieve(self, request, pk=None,**kwargs):
        queryset = self.get_event_list()
        for item in queryset:
            if int(item['id']) == int(pk):
                return Response(data=item)
        raise NotFound() 


class EventUserViewSet(EventMixin,ModelViewSet):
    """
    A viewset for viewing and editing Events.
    """
    queryset = EventUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return EventUserCreateSerializer
        return EventUserSerializer

    @staticmethod
    def check_permission(request,fuser):
        if request.user == fuser or request.user.is_superuser:
            return True
        else:
            raise PermissionDenied()

    def get_event(self,event_id):
        event = get_object_or_404(Event,pk=event_id)
        queryset = self.get_event_list()
        for item in queryset:
            if int(item['id']) == int(event.id):
                return item
        raise NotFound()

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user = get_object_or_404(User,pk=data['user_id'])
            event = get_object_or_404(Event,pk=data['event_id'])
            self.check_permission(request=request,fuser=user)
            try:
                new_eventuser_obj = EventUser.objects.create(event=event,user=user,action=data['action'])
            except DataError as e:
                raise ObjectExistsException(detail=e) 
            else:
                event_id = new_eventuser_obj.event.id
                return Response(data={"created":data,'event':self.get_event(event_id)},status=status.HTTP_201_CREATED)
        else:
            #raise Serializer Exception
            super().create(request, *args, **kwargs)


    def update(self,request,*args,**kwargs):

        #get eventuser to check permissions
        event_user = get_object_or_404(EventUser,pk=kwargs.get('pk'))
        self.check_permission(request=request,fuser=event_user.user)
        super().update(request,*args,**kwargs)

        #get event user again with new action
        event_user = get_object_or_404(EventUser,pk=kwargs.get('pk'))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=event_user)
        data = serializer.data
        data.update({'event':self.get_event(event_user.event.id)})
        return Response(data=data,status=status.HTTP_200_OK)

    def retrieve(self, request, *args,**kwargs):
        super().retrieve(request, *args, **kwargs)

        event_user = get_object_or_404(EventUser,pk=kwargs.get('pk'))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=event_user)
        data = serializer.data
        data.update({'event':self.get_event(event_user.event.id)})
        return Response(data=data,status=status.HTTP_200_OK)