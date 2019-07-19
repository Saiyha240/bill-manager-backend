from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.db import transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.events.models import Event, Guest, GuestType
from api.users.serializers import UserBasicSerializer

User = get_user_model()


class GuestSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='user'
    )
    user = UserBasicSerializer(read_only=True)

    class Meta:
        model = Guest
        fields = ('user', 'type', 'user_id')
        extra_kwargs = {
            'email': {
                'validators': [EmailValidator()]
            }
        }


class EventSerializer(serializers.HyperlinkedModelSerializer):
    guests = GuestSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Event
        fields = ('id', 'name', 'time_start', 'time_end', 'guests', 'url')

    def create(self, validated_data):
        guests = validated_data.pop('guests', [])

        try:
            with transaction.atomic():
                event = super().create(validated_data)

                current_user = self.context['request'].user
                event.guests.create(user=current_user, type=GuestType.ADMINISTRATOR)

                for user in guests:
                    event.guests.create(**user)

                return event
        except Exception as e:
            raise serializers.ValidationError(e)

    def validate(self, attrs):
        time_start = attrs['time_start']
        time_end = attrs['time_end']

        if time_start < timezone.now():
            raise ValidationError(_('"time_start" is already over'))

        if time_end <= time_start:
            raise ValidationError(_('"time_start" cannot be after "time_end"'))

        return super().validate(attrs)
