# Create your tests here.


from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from api.authentication.models import User
from api.authentication.serializers import UserSerializer
from api.authentication.views import UserRetrieveUpdateAPIView


class UserModelTest(TestCase):
    def test_profile_created_for_created_user(self):
        user = User.objects.create(email='test@email.com', username='test_user')

        self.assertTrue(hasattr(user, 'profile'))


class UserViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(email='test1@email.com', username='test_user1')
        cls.user_2 = User.objects.create(email='test2@email.com', username='test_user2')

    def setUp(self) -> None:
        self.client = APIRequestFactory()
        self.user_1.refresh_from_db()
        self.user_2.refresh_from_db()

    def test_get_user(self):
        request = self.client.get(reverse('current-user-detail'))
        force_authenticate(request, self.user_1)
        view = UserRetrieveUpdateAPIView.as_view()

        response = view(request)

        serializer = UserSerializer(self.user_1)

        self.assertEquals(serializer.data, response.data)

    def test_unauthenticated_get_user_fails(self):
        request = self.client.get(reverse('current-user-detail'))
        view = UserRetrieveUpdateAPIView.as_view()

        response = view(request)

        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_unauthenticated_update_user_profile_fails(self):
        new_profile = {
            'username': self.user_1.username,
            'email': self.user_1.email,
            'bio': 'Updated Bio'
        }

        request = self.client.patch(reverse('current-user-detail'), data=new_profile)
        view = UserRetrieveUpdateAPIView.as_view()

        self.assertEquals('', self.user_1.profile.bio)

        response = view(request)

        self.assertEquals('', self.user_1.profile.bio)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_update_user_profile(self):
        new_profile = {
            'username': self.user_1.username,
            'email': self.user_1.email,
            'bio': 'Updated Bio'
        }

        request = self.client.patch(reverse('current-user-detail'), data=new_profile)
        force_authenticate(request, self.user_1)
        view = UserRetrieveUpdateAPIView.as_view()

        self.assertEquals('', self.user_1.profile.bio)

        response = view(request)

        serializer = UserSerializer(self.user_1)

        self.assertEquals(serializer.data, response.data)
        self.assertEquals(new_profile['bio'], self.user_1.profile.bio)

    def test_update_user_profile_not_matching_user_fails(self):
        new_profile = {
            'username': self.user_2.username,
            'email': self.user_2.email,
            'bio': 'Updated Bio'
        }

        request = self.client.patch(reverse('current-user-detail'), data=new_profile)
        force_authenticate(request, self.user_1)
        view = UserRetrieveUpdateAPIView.as_view()

        self.assertEquals('', self.user_1.profile.bio)

        response = view(request)

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertNotEquals(new_profile['bio'], self.user_1.profile.bio)
