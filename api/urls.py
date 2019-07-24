from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

# router = routers.DefaultRouter()
#
# router.register('users', UserViewSet, 'user')
# router.register('events', EventViewSet, 'event')
# router.register('orders', OrderViewSet, 'order')
#
# users_router = routers.NestedSimpleRouter(router, 'users', lookup='user')
# users_router.register('events', UserEventViewSet, base_name='user-events')
# # users_router.register('orders', EventUserViewSet, base_name='user-orders')
#
# events_router = routers.NestedSimpleRouter(router, 'events', lookup='event')
# events_router.register('users', EventUserViewSet, base_name='event-users')
# events_router.register('orders', EventOrderViewSet, base_name='event-orders')

urlpatterns = [
    # path('api/v1/', include(router.urls)),
    # path('api/v1/', include(users_router.urls)),
    # path('api/v1/', include(events_router.urls)),
    path('api/v1/', include('api.authentication.urls')),
    path('api/v1/', include('api.profiles.urls')),
    path('api/v1/', include('api.events.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
# for url in urlpatterns:
#     print(str(url), '\n')
