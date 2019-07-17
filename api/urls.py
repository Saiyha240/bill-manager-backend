from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.events.views import EventView
from api.orders.views import OrderView

router = DefaultRouter()

router.register('events', EventView)
router.register('orders', OrderView)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('api.users.urls'))
]
