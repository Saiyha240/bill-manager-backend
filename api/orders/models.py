from django.contrib.auth import get_user_model
from django.db import models
# Create your models here.
from django_extensions.db.models import TimeStampedModel

from api.events.models import Event

User = get_user_model()


class Order(TimeStampedModel):
    name = models.CharField(max_length=255)
    total = models.DecimalField(decimal_places=3, max_digits=12)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    event = models.ForeignKey(Event, related_name='orders', on_delete=models.CASCADE)

    users = models.ManyToManyField(User, through='OrderUser', related_name='orders')

    def __str__(self):
        return self.name


class OrderUser(models.Model):
    user = models.ForeignKey(User, related_name='user_orders', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='order_users', on_delete=models.CASCADE)

    order_amount = models.DecimalField(decimal_places=3, max_digits=12)
    paid_amount = models.DecimalField(decimal_places=3, max_digits=12, default=0)


class OrderHistory(models.Model):
    pass
