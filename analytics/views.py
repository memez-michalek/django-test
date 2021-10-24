# from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from analytics.serializers import EventSerializer
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from analytics.models import Event
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from analytics.authentication import BearerAuthentication
from django.utils import timezone

class EventCreate(APIView):
    def create(self,request,*args, **kwargs):
        event_name = request.data.get('name')
        additional_data = request.data.get('additional_data')
        api_key = request.headers['Authorization'].split(' ')[1]
        
        if event_name is None or event_name=='' or len(event_name) > 255:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'event name is required'})        
        elif additional_data is None:
            additional_data = ''

        user_from_token = Token.objects.get(key=api_key).user
        event = Event.objects.create(name=event_name, 
                                    additional_data=additional_data, 
                                    created_at=timezone.now(),
                                    created_by=user_from_token)
        event.save()
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class EventView(EventCreate, CreateModelMixin):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    authentication_classes = [BearerAuthentication]
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
