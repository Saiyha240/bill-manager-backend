from rest_framework import serializers

from api.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    users = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='user-detail'
    )

    class Meta:
        model = Event
        fields = ('id', 'name', 'start_time', 'end_time', 'users')
