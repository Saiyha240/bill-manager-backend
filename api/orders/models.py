from django.db import models
# Create your models here.
from django_extensions.db.models import TimeStampedModel

from api.events.models import Event
from api.users.models import User


class Order(TimeStampedModel):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(decimal_places=3, max_digits=12)
    paid = models.BooleanField(default=False)

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='orders', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
