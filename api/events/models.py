from django.contrib.auth import get_user_model
from django.db import models
from django_enumfield import enum
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class GuestType(enum.Enum):
    ADMINISTRATOR = 1
    ORGANIZER = 2
    GUEST = 3


class Event(TimeStampedModel):
    name = models.CharField(max_length=32)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    # host = models.ForeignKey(User, related_name='hosts', null=True, on_delete=models.SET_NULL)

    users = models.ManyToManyField(User, through='Guest', related_name='events', blank=True)

    class Meta:
        ordering = ('-time_start',)

    def __str__(self):
        return self.name


class Guest(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="guest_events", null=True)
    event = models.ForeignKey(Event, related_name="guests", on_delete=models.SET_NULL, null=True, blank=True)
    type = enum.EnumField(GuestType, default=GuestType.GUEST)

    # is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = [['user', 'event']]
