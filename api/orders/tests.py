# # Create your tests here.
# from datetime import timedelta
#
# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.utils import timezone
#
# from api.events.models import Event, Guest
# from api.orders.models import Order, OrderUser
#
# User = get_user_model()
#
#
# class OrderTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user_1 = User.objects.create(username='user1', email='user1@email.com')
#         cls.user_2 = User.objects.create(username='user2', email='user2@email.com')
#         cls.user_3 = User.objects.create(username='user3', email='user3@email.com')
#
#         cls.event_1 = Event.objects.create(
#             name='event1',
#             time_start=timezone.now() + timedelta(days=1),
#             time_end=timezone.now() + timedelta(days=1, hours=1),
#         )
#         cls.event_2 = Event.objects.create(
#             name='event2',
#             time_start=timezone.now() + timedelta(days=2),
#             time_end=timezone.now() + timedelta(days=2, hours=1)
#         )
#
#         cls.order_1 = Order.objects.create(name='order_1', total=1000, event=cls.event_1, owner=cls.user_1)
#         cls.order_2 = Order.objects.create(name='order_2', total=1500, event=cls.event_1, owner=cls.user_2)
#         cls.order_3 = Order.objects.create(name='order_3', total=2000, event=cls.event_2, owner=cls.user_1)
#         cls.order_4 = Order.objects.create(name='order_4', total=2500, event=cls.event_2, owner=cls.user_2)
#
#     def setUp(self) -> None:
#         self.user_1.refresh_from_db()
#         self.user_2.refresh_from_db()
#         self.user_3.refresh_from_db()
#
#         self.event_1.refresh_from_db()
#         self.event_2.refresh_from_db()
#
#         self.order_1.refresh_from_db()
#         self.order_2.refresh_from_db()
#         self.order_3.refresh_from_db()
#         self.order_4.refresh_from_db()
#
#         Guest.objects.create(user=self.user_1, event=self.event_1, is_admin=False)
#         Guest.objects.create(user=self.user_2, event=self.event_1, is_admin=False)
#         Guest.objects.create(user=self.user_3, event=self.event_1, is_admin=False)
#
#         Guest.objects.create(user=self.user_1, event=self.event_2, is_admin=True)
#         Guest.objects.create(user=self.user_2, event=self.event_2, is_admin=False)
#
#     def test_get_user_orders(self):
#         order_user_1 = OrderUser.objects.create(order=self.order_1, user=self.user_1, order_amount=self.order_1.total)
#         order_user_3 = OrderUser.objects.create(order=self.order_3, user=self.user_1, order_amount=1000)
#
#         user_1_orders = self.user_1.user_orders.all()
#
#         self.assertCountEqual(list(user_1_orders), [order_user_1, order_user_3])
#
#     def test_get_event_orders(self):
#         order_user_1 = OrderUser.objects.create(order=self.order_1, user=self.user_1, order_amount=self.order_1.total)
#         order_user_3 = OrderUser.objects.create(order=self.order_2, user=self.user_1, order_amount=1000)
#
#         event_1_orders = self.event_1.orders.all()
#
#         self.assertCountEqual(list(event_1_orders), [self.order_1, self.order_2])
