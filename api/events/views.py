# Create your views here.
from rest_framework import viewsets

from api.events.models import Event
from api.events.serializers import EventSerializer


class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    class Meta:
        ordering = ('start_time',)
