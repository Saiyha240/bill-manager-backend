from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # path('users/', UserList.as_view(), name="user-list"),
    # path('users/<int:pk>/', UserDetail.as_view(), name="user-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
