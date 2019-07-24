from django.urls import path

from api.profiles.views import ProfileRetrieveAPIView

urlpatterns = [
    path('profiles/<username>/', ProfileRetrieveAPIView.as_view(), name='profile-detail')
]

# urlpatterns = format_suffix_patterns(urlpatterns)
