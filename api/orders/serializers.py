from rest_framework import serializers

from api.events.models import Event
from api.orders.models import Order
from api.users.models import User


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), many=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'amount', 'paid', 'user', 'event')
