# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.events.models import Event, MemberType
from api.events.permissions import EventPermissions
from api.events.serializers import EventSerializer, EventUpdateSerializer, MemberSerializer, EventJoinSerializer


class EventJoinView(generics.GenericAPIView):
    serializer_class = EventJoinSerializer

    def post(self, request, pk, *args, **kwargs):
        serializer_data = {
            "event": pk,
            "user": request.user.pk,
            "type": request.data.get('type', MemberType.GUEST)
        }

        serializer = self.get_serializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class EventListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class UserEventListCreateView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, EventPermissions)
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(attendees=self.kwargs['user_pk'])


class EventRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, EventPermissions)
    serializer_class = EventUpdateSerializer
    queryset = Event.objects.all()

    def update(self, request, *args, **kwargs):
        request_data = request.data
        event = self.get_object()

        serializer_data = {
            'name': request_data.get('name', event.name),
            'time_start': request_data.get('time_start', event.time_start),
            'time_end': request_data.get('time_end', event.time_end),
            'members': request_data.get('members', MemberSerializer(event.members, many=True).data)
        }

        serializer = self.serializer_class(event, data=serializer_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
