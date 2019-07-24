# Create your views here.
from rest_framework import status, generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.profiles.models import Profile
from api.profiles.serializers import ProfileSerializer


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username does not exist.')

        serializer = self.serializer_class(profile, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)
