from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # path('events/', EventList.as_view(), name="event-list"),
    # path('events/<int:pk>/', EventList.as_view(), name="event-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
