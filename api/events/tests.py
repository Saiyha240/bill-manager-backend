from datetime import timedelta

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from api.events.models import Event, Member, MemberType, User
from api.events.serializers import EventSerializer
from api.events.views import EventListCreateView, UserEventListCreateView, EventJoinView, EventRetrieveUpdateView


class EventUsersM2MTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(username='user1', email='user1@email.com')
        cls.user_2 = User.objects.create(username='user2', email='user2@email.com')
        cls.user_3 = User.objects.create(username='user3', email='user3@email.com')

        cls.event_1 = Event.objects.create(
            name='event1',
            time_start=timezone.now() + timedelta(days=1),
            time_end=timezone.now() + timedelta(days=1, hours=1)
        )
        cls.event_2 = Event.objects.create(
            name='event2',
            time_start=timezone.now() + timedelta(days=2),
            time_end=timezone.now() + timedelta(days=2, hours=1)
        )
        cls.event_3 = Event.objects.create(
            name='event3',
            time_start=timezone.now() + timedelta(days=3),
            time_end=timezone.now() + timedelta(days=3, hours=1)
        )

    def setUp(self) -> None:
        self.user_1.refresh_from_db()
        self.user_2.refresh_from_db()
        self.user_3.refresh_from_db()

        self.event_1.refresh_from_db()
        self.event_2.refresh_from_db()
        self.event_3.refresh_from_db()

        Member.objects.create(user=self.user_1, event=self.event_1, type=MemberType.ADMINISTRATOR)
        Member.objects.create(user=self.user_2, event=self.event_1, type=MemberType.GUEST)
        Member.objects.create(user=self.user_3, event=self.event_1, type=MemberType.GUEST)

        Member.objects.create(user=self.user_1, event=self.event_2, type=MemberType.ADMINISTRATOR)
        Member.objects.create(user=self.user_2, event=self.event_2, type=MemberType.ORGANIZER)
        Member.objects.create(user=self.user_3, event=self.event_2, type=MemberType.GUEST)

        Member.objects.create(user=self.user_2, event=self.event_3, type=MemberType.ADMINISTRATOR)

    def test_get_user_1_hosted_events(self):
        user_1_hosted_events = list(self.user_1.events.filter(members__type=MemberType.ADMINISTRATOR))

        self.assertCountEqual([self.event_1, self.event_2], user_1_hosted_events)

    def test_get_user_2_non_hosted_events(self):
        user_2_non_hosted_events = list(self.user_2.events.filter(members__type__in=[
            MemberType.ORGANIZER,
            MemberType.GUEST
        ]))

        self.assertCountEqual([self.event_1, self.event_2], user_2_non_hosted_events)

    def test_add_existing_user_in_event_fails(self):
        parameters = dict(user=self.user_1, event=self.event_1)

        self.assertRaises(IntegrityError, Member.objects.create, **parameters)

    def test_remove_user_2_in_event_1(self):
        user_2_events = self.user_2.events.all()
        self.assertCountEqual(list(user_2_events), [self.event_1, self.event_2, self.event_3])

        Event.objects.get(attendees=self.user_2, pk=self.event_1.id).delete()
        user_2_events = user_2_events.all()

        self.assertCountEqual([self.event_2, self.event_3], list(user_2_events))

    def test_update_set_user_2_as_organizer_in_event_1(self):
        guest_obj = Member.objects.get(user=self.user_2, event=self.event_1)

        self.assertEquals(guest_obj.type, MemberType.GUEST)

        guest_obj.type = MemberType.ORGANIZER
        guest_obj.save()

        self.assertEquals(MemberType.ORGANIZER, guest_obj.type)

    def test_add_user_3_to_event_3_defaults_as_guest_type(self):
        self.event_3.members.create(user=self.user_3)

        self.assertIn(self.user_3, list(self.event_3.attendees.filter(member__type=MemberType.GUEST)))

    def test_add_user_1_to_event_3_as_organizer_type(self):
        self.event_3.members.create(user=self.user_1, type=MemberType.ORGANIZER)

        self.assertIn(self.user_1, list(self.event_3.attendees.filter(member__type=MemberType.ORGANIZER)))


class EventViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(username='user1', email='user1@email.com')
        cls.user_2 = User.objects.create(username='user2', email='user2@email.com')
        cls.user_3 = User.objects.create(username='user3', email='user3@email.com')

        cls.event_1 = Event.objects.create(
            name='event1',
            time_start=timezone.now() + timedelta(days=1),
            time_end=timezone.now() + timedelta(days=1, hours=1),
        )
        cls.event_2 = Event.objects.create(
            name='event2',
            time_start=timezone.now() + timedelta(days=2),
            time_end=timezone.now() + timedelta(days=2, hours=1)
        )
        cls.event_3 = Event.objects.create(
            name='event3',
            time_start=timezone.now() + timedelta(days=3),
            time_end=timezone.now() + timedelta(days=3, hours=1)
        )

    def setUp(self) -> None:
        self.client = APIRequestFactory()

        self.user_1.refresh_from_db()
        self.user_2.refresh_from_db()
        self.user_3.refresh_from_db()

        self.event_1.refresh_from_db()
        self.event_2.refresh_from_db()
        self.event_3.refresh_from_db()

        self.event_1.members.create(user=self.user_1, type=MemberType.ADMINISTRATOR)
        self.event_2.members.create(user=self.user_2, type=MemberType.ADMINISTRATOR)
        self.event_3.members.create(user=self.user_3, type=MemberType.ADMINISTRATOR)

    def test_get_all_events(self):
        request = self.client.get(reverse('event-list'))
        force_authenticate(request, self.user_1)
        view = EventListCreateView.as_view()

        response = view(request)

        events = Event.objects.all()
        serializer = EventSerializer(events, many=True, context={'request': request})

        self.assertCountEqual(response.data, serializer.data)

    def test_create_event_no_guests(self):
        event_request = {
            "name": "Event 3",
            "time_start": "2020-08-11T20:17:46.384Z",
            "time_end": "2021-08-12T20:17:46.384Z"
        }

        request = self.client.post(reverse('event-list'), event_request)
        force_authenticate(request, self.user_1)
        view = EventListCreateView.as_view()

        response = view(request)

        event = Event.objects.get(pk=response.data['id'])
        serializer = EventSerializer(event, context={'request': request})

        self.assertDictEqual(response.data, serializer.data)

    def test_create_event_with_guests(self):
        event_request = {
            "name": "Event 3",
            "time_start": "2020-08-11T20:17:46.384Z",
            "time_end": "2021-08-12T20:17:46.384Z",
            "members": [
                {
                    "user": self.user_2.pk
                }
            ]
        }

        request = self.client.post(reverse('event-list'), event_request)
        force_authenticate(request, self.user_1)
        view = EventListCreateView.as_view()

        response = view(request)

        event = Event.objects.get(pk=response.data['id'])
        serializer = EventSerializer(event, context={'request': request})

        self.assertDictEqual(response.data, serializer.data)

    def test_get_user_events(self):
        kwargs = {'user_pk': self.user_1.pk}

        request = self.client.get(reverse('user-event-list', kwargs=kwargs))
        force_authenticate(request, self.user_1)
        view = UserEventListCreateView.as_view()

        response = view(request, **kwargs)

        serializer = EventSerializer(self.user_1.events, many=True)

        self.assertEquals(serializer.data, response.data)

    def test_user_joins_event(self):
        kwargs = {'pk': self.event_2.pk}

        request = self.client.post(reverse('event-join', kwargs=kwargs))
        force_authenticate(request, self.user_1)
        view = EventJoinView.as_view()

        self.assertNotIn(self.user_1, list(self.event_2.attendees.all()))

        response = view(request, **kwargs)

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertIn(self.user_1, list(self.event_2.attendees.all()))

    def test_user_joins_already_joined_event_error(self):
        Member.objects.create(event=self.event_2, user=self.user_1)

        kwargs = {'pk': self.event_2.pk}

        request = self.client.post(reverse('event-join', kwargs=kwargs))
        force_authenticate(request, self.user_1)
        view = EventJoinView.as_view()

        self.assertIn(self.user_1, list(self.event_2.attendees.all()))

        response = view(request, **kwargs)

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_event(self):
        self.event_1.members.create(user=self.user_2)
        self.event_2.members.create(user=self.user_3)

        kwargs = {'pk': self.event_1.pk}
        data = {
            'time_start': self.event_1.time_start - timedelta(hours=1)
        }

        request = self.client.patch(reverse('event-detail', kwargs=kwargs), data=data)
        force_authenticate(request, self.user_1)
        view = EventRetrieveUpdateView.as_view()

        response = view(request, **kwargs)

        self.event_1.refresh_from_db()
        serializer = EventSerializer(self.event_1)

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer.data, response.data)

    def test_update_event_with_members(self):
        kwargs = {'pk': self.event_1.pk}
        data = {
            'members': [
                {
                    'user': self.user_2.pk,
                    'type': MemberType.ORGANIZER
                }
            ]
        }

        request = self.client.patch(reverse('event-detail', kwargs=kwargs), data=data)
        force_authenticate(request, self.user_1)
        view = EventRetrieveUpdateView.as_view()

        response = view(request, **kwargs)

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertIn(self.user_2, list(self.event_1.attendees.all()))

    def test_add_multiple_users_to_event(self):
        kwargs = {'pk': self.event_1.pk}
        data = {
            'members': [
                {
                    'user': self.user_2.pk,
                    'type': MemberType.ORGANIZER
                },
                {
                    'user': self.user_3.pk
                }
            ]
        }

        request = self.client.patch(reverse('event-detail', kwargs=kwargs), data=data)
        force_authenticate(request, self.user_1)
        view = EventRetrieveUpdateView.as_view()

        response = view(request, **kwargs)

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertIn(self.user_2, list(self.event_1.attendees.all()))
        self.assertIn(self.user_3, list(self.event_1.attendees.all()))
