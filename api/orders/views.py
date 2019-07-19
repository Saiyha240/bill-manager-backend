# Create your views here.
from rest_framework import viewsets

from api.orders.models import Order
from api.orders.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class EventOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(event=self.kwargs['event_pk'])
