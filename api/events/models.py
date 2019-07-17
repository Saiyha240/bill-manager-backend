from django.db import models
from django_extensions.db.models import TimeStampedModel

from api.users.models import User


class Event(TimeStampedModel):
    name = models.CharField(max_length=32)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    users = models.ManyToManyField(User, through='EventUser', related_name="events", blank=True)

    def __str__(self):
        return self.name


class EventUser(models.Model):
    user = models.ForeignKey(User, related_name="event_users", on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, related_name="event_users", on_delete=models.SET_NULL, null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = [['user', 'event']]
