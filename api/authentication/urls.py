from django.urls import path

from api.authentication.views import UserRetrieveUpdateAPIView

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='current-user-detail')
    # path('users/', UserList.as_view(), name="user-list"),
    # path('users/<int:pk>/', UserDetail.as_view(), name="user-detail"),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
