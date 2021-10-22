# from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from analytics.serializers import EventSerializer
from rest_framework.mixins import CreateModelMixin
from analytics.models import Event


class EventView(CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
