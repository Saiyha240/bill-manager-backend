from django.db import IntegrityError
from django.test import TestCase
# Create your tests here.
from django.utils import timezone

from api.events.models import Event, EventUser
from api.users.models import User


class EventUsersM2MTest(TestCase):
    def setUp(self) -> None:
        self.user_1 = User.objects.create(username='user1', email='user1@email.com')
        self.user_2 = User.objects.create(username='user2', email='user2@email.com')
        self.user_3 = User.objects.create(username='user2', email='user3@email.com')

        self.event_1 = Event.objects.create(name='event1', start_time=timezone.now(), end_time=timezone.now())
        self.event_2 = Event.objects.create(name='event2', start_time=timezone.now(), end_time=timezone.now())
        self.event_3 = Event.objects.create(name='event3', start_time=timezone.now(), end_time=timezone.now())

        EventUser.objects.create(user=self.user_1, event=self.event_1, is_admin=False)
        EventUser.objects.create(user=self.user_2, event=self.event_1, is_admin=False)
        EventUser.objects.create(user=self.user_3, event=self.event_1, is_admin=False)

        EventUser.objects.create(user=self.user_1, event=self.event_2, is_admin=True)
        EventUser.objects.create(user=self.user_2, event=self.event_2, is_admin=False)

    def test_user_1_is_part_of_event_1(self):
        user_1_groups = Event.objects.filter(users=self.user_1)

        self.assertEquals(list(user_1_groups), [self.event_2, self.event_1])

    def test_user_1_admin_groups(self):
        user_1_admin_groups = Event.objects.filter(users=self.user_1, event_users__is_admin=True)

        self.assertEquals(list(user_1_admin_groups), [self.event_2])

    def test_add_existing_user_in_event_fails(self):
        self.assertRaises(IntegrityError, EventUser.objects.create, user=self.user_1, event=self.event_1)

    def test_remove_user_2_in_event_1(self):
        user_2_events = Event.objects.filter(users=self.user_2)
        self.assertEquals(list(user_2_events), [self.event_2, self.event_1])

        Event.objects.get(users=self.user_2, pk=self.event_1.id).delete()
        user_2_events = user_2_events.all()

        self.assertEquals(list(user_2_events), [self.event_2])

    def test_update_set_user_1_as_admin_in_event_1(self):
        event_user = EventUser.objects.get(user=self.user_1, event=self.event_1)

        event_user.is_admin = True

        event_user.save()

        self.assertTrue(event_user.is_admin)
