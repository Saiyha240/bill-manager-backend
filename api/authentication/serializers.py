from rest_framework import serializers

from api.authentication.models import User
from api.profiles.serializers import ProfileSerializer


# class UserBasicSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#
#         fields = ('id', 'username', 'email', 'url')
#
#
# class EventBasicSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = ('id', 'name', 'time_end', 'time_start')
#
#
# class GuestEventSerializer(serializers.ModelSerializer):
#     event = EventBasicSerializer()
#
#     class Meta:
#         model = Guest
#         fields = ('user', 'type', 'user_id')
#         extra_kwargs = {
#             'email': {
#                 'validators': [EmailValidator()]
#             }
#         }
#
#
# class UserListSerializer(serializers.ModelSerializer):
#     events = serializers.HyperlinkedRelatedField(
#         many=True,
#         view_name='event-detail',
#         read_only=True
#     )
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'events')
#
#
# class NestedUserListSerializer(UserListSerializer):
#     class Meta(UserListSerializer.Meta):
#         extra_kwargs = {
#             'email': {
#                 'validators': []
#             }
#         }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    profile = ProfileSerializer(write_only=True)

    bio = serializers.CharField(source='profile.bio', read_only=True)
    image = serializers.CharField(source='profile.image', read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'profile', 'bio', 'image')

    def update(self, instance: User, validated_data):
        password = validated_data.pop('password', None)

        profile_data = validated_data.pop('profile', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        for key, value in profile_data.items():
            setattr(instance.profile, key, value)

        instance.profile.save()

        return instance
