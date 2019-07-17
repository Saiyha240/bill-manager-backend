from rest_framework import serializers

from api.users.models import User


class UserSerializer(serializers.ModelSerializer):
    events = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='event-detail',
        read_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'events')
