# Create your views here.
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.authentication.serializers import UserSerializer


# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class EventUserViewSet(mixins.CreateModelMixin,
#                        mixins.RetrieveModelMixin,
#                        mixins.ListModelMixin,
#                        viewsets.GenericViewSet):
#     serializer_class = GuestUserSerializer
#
#     def perform_create(self, serializer):
#         super().perform_create(serializer)
#
#     # permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         return Guest.objects.filter(event=self.kwargs['event_pk'])
#
#
# class OrderUserViewSet(mixins.CreateModelMixin,
#                        mixins.RetrieveModelMixin,
#                        mixins.ListModelMixin,
#                        viewsets.GenericViewSet):
#     serializer_class = UserBasicSerializer
#
#
# class UserViewSet(mixins.CreateModelMixin,
#                   mixins.RetrieveModelMixin,
#                   mixins.ListModelMixin,
#                   viewsets.GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserListSerializer
#     # permission_classes = [permissions.IsAuthenticated]

class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        request_data = request.data

        serializer_data = {
            'username': request_data.get('username', request.user.username),
            'email': request_data.get('email', request.user.email),
            'profile': {
                'bio': request_data.get('bio', request.user.profile.bio),
                'image': request_data.get('image', request.user.profile.image),
            }
        }

        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
