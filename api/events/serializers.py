from django.db import transaction, IntegrityError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.events.models import Event, Member, MemberType


class EventJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('user', 'event', 'type')

    def create(self, validated_data):
        try:
            member = Member.objects.create(**validated_data)

            return member

        except IntegrityError as e:
            return ValidationError(_('already joined'))


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'user', 'type')


class EventSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, required=False)
    time_start = serializers.DateTimeField(required=False)
    time_end = serializers.DateTimeField(required=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'time_start', 'time_end', 'members')

    def create(self, validated_data):
        members = validated_data.pop('members', [])

        try:
            with transaction.atomic():
                event = super().create(validated_data)

                current_user = self.context['request'].user
                event.members.create(user=current_user, type=MemberType.ADMINISTRATOR)

                for user in members:
                    if 'type' in user and user['type'] == MemberType.ADMINISTRATOR:
                        raise ValidationError(_(f'user cannot be set as {MemberType.ADMINISTRATOR.lower()}'))
                    event.members.create(**user)

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


class EventUpdateSerializer(EventSerializer):
    members = MemberSerializer(many=True)

    def update(self, instance, validated_data):
        to_update_members = validated_data.pop('members', [])

        try:
            with transaction.atomic():
                event = super().update(instance, validated_data)
                event_members = set(member.id for member in event.members.all() if
                                    member.type is not MemberType.ADMINISTRATOR)

                for to_update_member in to_update_members:

                    member, created = event.members.get_or_create(user=to_update_member['user'])
                    member.type = to_update_member.get('type', member.type)
                    member.save()

                    if not created:
                        event_members.discard(member.id)

                event.members.filter(id__in=event_members).delete()

            return event
        except Exception as e:
            raise serializers.ValidationError(e)
