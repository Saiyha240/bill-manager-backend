from rest_framework import viewsets, mixins

# Create your views here.
from api.users.models import User
from api.users.serializers import UserSerializer


# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class EventUserViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)

    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(events=self.kwargs['event_pk'])


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
