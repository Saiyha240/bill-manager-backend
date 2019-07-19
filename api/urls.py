from django.urls import path, include
from rest_framework_nested import routers

from api.events.views import EventViewSet, UserEventViewSet
from api.orders.views import OrderViewSet, EventOrderViewSet
from api.users.views import UserViewSet, EventUserViewSet

router = routers.DefaultRouter()

router.register('users', UserViewSet, 'user')
router.register('events', EventViewSet, 'event')
router.register('orders', OrderViewSet, 'order')

users_router = routers.NestedSimpleRouter(router, 'users', lookup='user')
users_router.register('events', UserEventViewSet, base_name='user-events')
# users_router.register('orders', EventUserViewSet, base_name='user-orders')

events_router = routers.NestedSimpleRouter(router, 'events', lookup='event')
events_router.register('users', EventUserViewSet, base_name='event-users')
events_router.register('orders', EventOrderViewSet, base_name='event-orders')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(users_router.urls)),
    path('api/v1/', include(events_router.urls)),
]

# for url in router.urls + users_router.urls:
#     print(str(url), '\n')
