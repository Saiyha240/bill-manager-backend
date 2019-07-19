from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIRequestFactory, force_authenticate

from api.events.models import Event, Guest, GuestType
from api.events.serializers import EventSerializer
from api.events.views import EventViewSet

User = get_user_model()


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

        Guest.objects.create(user=self.user_1, event=self.event_1, type=GuestType.ADMINISTRATOR)
        Guest.objects.create(user=self.user_2, event=self.event_1, type=GuestType.GUEST)
        Guest.objects.create(user=self.user_3, event=self.event_1, type=GuestType.GUEST)

        Guest.objects.create(user=self.user_1, event=self.event_2, type=GuestType.ADMINISTRATOR)
        Guest.objects.create(user=self.user_2, event=self.event_2, type=GuestType.ORGANIZER)
        Guest.objects.create(user=self.user_3, event=self.event_2, type=GuestType.GUEST)

        Guest.objects.create(user=self.user_2, event=self.event_3, type=GuestType.ADMINISTRATOR)

    def test_get_user_1_hosted_events(self):
        user_1_hosted_events = list(self.user_1.events.filter(guests__type=GuestType.ADMINISTRATOR))

        self.assertCountEqual(user_1_hosted_events, [self.event_1, self.event_2])

    def test_get_user_2_non_hosted_events(self):
        user_2_non_hosted_events = list(self.user_2.events.filter(guests__type__in=[
            GuestType.ORGANIZER,
            GuestType.GUEST
        ]))

        self.assertCountEqual(user_2_non_hosted_events, [self.event_1, self.event_2])

    def test_add_existing_user_in_event_fails(self):
        parameters = dict(user=self.user_1, event=self.event_1)

        self.assertRaises(IntegrityError, Guest.objects.create, **parameters)

    def test_remove_user_2_in_event_1(self):
        user_2_events = Event.objects.filter(users=self.user_2)
        self.assertCountEqual(list(user_2_events), [self.event_1, self.event_2, self.event_3])

        Event.objects.get(users=self.user_2, pk=self.event_1.id).delete()
        user_2_events = user_2_events.all()

        self.assertCountEqual(list(user_2_events), [self.event_2, self.event_3])

    def test_update_set_user_2_as_organizer_in_event_1(self):
        guest_obj = Guest.objects.get(user=self.user_2, event=self.event_1)

        self.assertEquals(guest_obj.type, GuestType.GUEST)

        guest_obj.type = GuestType.ORGANIZER
        guest_obj.save()

        self.assertEquals(guest_obj.type, GuestType.ORGANIZER)

    def test_add_user_3_to_event_3_defaults_as_guest_type(self):
        self.event_3.guests.create(user=self.user_3)

        self.assertIn(self.user_3, list(self.event_3.users.filter(guest_events__type=GuestType.GUEST)))

    def test_add_user_1_to_event_3_as_organizer_type(self):
        self.event_3.guests.create(user=self.user_1, type=GuestType.ORGANIZER)

        self.assertIn(self.user_1, list(self.event_3.users.filter(guest_events__type=GuestType.ORGANIZER)))


class EventIntegrationTest(TestCase):
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
        self.user_1.refresh_from_db()
        self.user_2.refresh_from_db()
        self.user_3.refresh_from_db()

        self.event_1.refresh_from_db()
        self.event_2.refresh_from_db()
        self.event_3.refresh_from_db()

        self.event_1.guests.create(user=self.user_1, type=GuestType.ADMINISTRATOR)
        self.event_2.guests.create(user=self.user_2, type=GuestType.ADMINISTRATOR)
        self.event_3.guests.create(user=self.user_3, type=GuestType.ADMINISTRATOR)

    def test_get_all_events(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('event-list'))
        force_authenticate(request, self.user_1)
        view = EventViewSet.as_view({'get': 'list'})

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
        factory = APIRequestFactory()
        request = factory.post(reverse('event-list'), event_request)
        force_authenticate(request, self.user_1)
        view = EventViewSet.as_view({'post': 'create'})

        response = view(request)

        event = Event.objects.get(pk=response.data['id'])
        serializer = EventSerializer(event, context={'request': request})

        self.assertDictEqual(response.data, serializer.data)

    def test_create_event_with_guests(self):
        event_request = {
            "name": "Event 3",
            "time_start": "2020-08-11T20:17:46.384Z",
            "time_end": "2021-08-12T20:17:46.384Z",
            "guests": [
                {
                    "user_id": self.user_2.pk,
                    "type": 2
                }
            ]
        }
        factory = APIRequestFactory()
        request = factory.post(reverse('event-list'), event_request)
        force_authenticate(request, self.user_1)
        view = EventViewSet.as_view({'post': 'create'})

        response = view(request)

        event = Event.objects.get(pk=response.data['id'])
        serializer = EventSerializer(event, context={'request': request})

        self.assertDictEqual(response.data, serializer.data)
