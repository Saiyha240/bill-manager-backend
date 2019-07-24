from django.urls import path

from api.events.views import EventListCreateView, EventRetrieveUpdateView, UserEventListCreateView, EventJoinView

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name="event-list"),
    path('events/<int:pk>/', EventRetrieveUpdateView.as_view(), name="event-detail"),
    path('events/<int:pk>/join', EventJoinView.as_view(), name="event-join"),
    path('users/<int:user_pk>/events/', UserEventListCreateView.as_view(), name="user-event-list"),
    # path('events/<int:pk>/join/', EventUserJoin.as_view(), name="event-user-join"),
]
