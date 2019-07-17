# Create your views here.
from rest_framework import viewsets

from api.orders.models import Order
from api.orders.serializers import OrderSerializer


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
