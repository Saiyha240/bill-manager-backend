from django.test import TestCase
# Create your tests here.
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from api.authentication.models import User
from api.profiles.serializers import ProfileSerializer
from api.profiles.views import ProfileRetrieveAPIView


class ProfileViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(email='test1@email.com', username='test_user1')

    def setUp(self) -> None:
        self.client = APIRequestFactory()
        self.user_1.refresh_from_db()

    def test_unauthenticated_get_profile(self):
        kwargs = {'username': self.user_1.username}

        request = self.client.get(reverse('profile-detail', kwargs=kwargs))
        view = ProfileRetrieveAPIView.as_view()

        response = view(request, **kwargs)

        serializer = ProfileSerializer(self.user_1.profile)

        self.assertEquals(serializer.data, response.data)

    # def test_unauthenticated_get_profile_fails(self):
    #     request = self.client.get(reverse('current-profile-detail'))
    #     view = ProfileRetrieveUpdateAPIView.as_view()
    #
    #     response = view(request)
    #
    #     self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)
    #
    # def test_unauthenticated_update_profile_profile_fails(self):
    #     new_profile = {
    #         'profilename': self.profile_1.profilename,
    #         'email': self.profile_1.email,
    #         'bio': 'Updated Bio'
    #     }
    #
    #     request = self.client.patch(reverse('current-profile-detail'), data=new_profile)
    #     view = ProfileRetrieveUpdateAPIView.as_view()
    #
    #     self.assertEquals('', self.profile_1.profile.bio)
    #
    #     response = view(request)
    #
    #     self.assertEquals('', self.profile_1.profile.bio)
    #     self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)
    #
    # def test_update_profile_profile(self):
    #     new_profile = {
    #         'profilename': self.profile_1.profilename,
    #         'email': self.profile_1.email,
    #         'bio': 'Updated Bio'
    #     }
    #
    #     request = self.client.patch(reverse('current-profile-detail'), data=new_profile)
    #     force_authenticate(request, self.profile_1)
    #     view = ProfileRetrieveUpdateAPIView.as_view()
    #
    #     self.assertEquals('', self.profile_1.profile.bio)
    #
    #     response = view(request)
    #
    #     serializer = ProfileSerializer(self.profile_1)
    #
    #     self.assertEquals(serializer.data, response.data)
    #     self.assertEquals(new_profile['bio'], self.profile_1.profile.bio)
    #
    # def test_update_profile_profile_not_matching_profile_fails(self):
    #     new_profile = {
    #         'profilename': self.profile_2.profilename,
    #         'email': self.profile_2.email,
    #         'bio': 'Updated Bio'
    #     }
    #
    #     request = self.client.patch(reverse('current-profile-detail'), data=new_profile)
    #     force_authenticate(request, self.profile_1)
    #     view = ProfileRetrieveUpdateAPIView.as_view()
    #
    #     self.assertEquals('', self.profile_1.profile.bio)
    #
    #     response = view(request)
    #
    #     self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
    #     self.assertNotEquals(new_profile['bio'], self.profile_1.profile.bio)
