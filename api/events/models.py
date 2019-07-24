from django.contrib.auth import get_user_model
from django.db import models
from django_enumfield import enum
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class MemberType(enum.Enum):
    ADMINISTRATOR = 1
    ORGANIZER = 2
    GUEST = 3


class Event(TimeStampedModel):
    name = models.CharField(max_length=32)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    # host = models.ForeignKey(User, related_name='hosts', null=True, on_delete=models.SET_NULL)

    attendees = models.ManyToManyField(User, through='Member', related_name='events')

    class Meta:
        ordering = ('-time_start',)

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='members')
    type = enum.EnumField(MemberType, default=MemberType.GUEST)

    class Meta:
        unique_together = [['user', 'event']]
        ordering = ['type', 'user__username']

    def __str__(self):
        return f'{self.event.name} - {self.user.username} - {self.type}'
