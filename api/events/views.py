# Create your views here.
from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from api.events.models import Event, Guest
from api.events.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(methods=['get'], detail=True, url_path='join', url_name='join')
    def join(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        current_user = request.user

        try:
            Guest.objects.create(user=current_user, event=event)

            serializer = self.get_serializer(event)

            return Response(serializer.data)
        except IntegrityError:
            return Response({"message": "Already joined"}, status=HTTP_400_BAD_REQUEST)


class UserEventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    # permission_classes = [permissions.IsAuthenticated]

    class Meta:
        ordering = ('start_time',)

    def get_queryset(self):
        return Event.objects.filter(users=self.kwargs['user_pk'])
