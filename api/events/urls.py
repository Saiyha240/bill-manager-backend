from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # path('events/', EventList.as_view(), name="event-list"),
    # path('events/<int:pk>/', EventDetail.as_view(), name="event-detail"),
    # path('events/<int:pk>/join/', EventUserJoin.as_view(), name="event-user-join"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
