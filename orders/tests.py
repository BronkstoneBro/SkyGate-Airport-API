from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.utils import timezone
from datetime import timedelta

from .models import Order
from .serializers import OrderSerializer
from tickets.models import Ticket
from flights.models import Flight, Crew
from airports.models import Airport, Route
from airplanes.models import Airplane, AirplaneType


class OrderModelTest(TestCase):
    """Tests for the Order model"""

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
        )

        self.source_airport = Airport.objects.create(
            name="JFK Airport", closest_big_city="New York"
        )
        self.destination_airport = Airport.objects.create(
            name="LAX Airport", closest_big_city="Los Angeles"
        )
        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.destination_airport,
            distance=3900,
        )
        self.airplane_type = AirplaneType.objects.create(
            name="Boeing 737", rows=30, seats_in_row=6
        )
        self.airplane = Airplane.objects.create(
            name="SG-1001", airplane_type=self.airplane_type
        )

        now = timezone.now()
        self.flight = Flight.objects.create(
            flight_number="SG123",
            departure_time=now + timedelta(hours=24),
            arrival_time=now + timedelta(hours=27),
            route=self.route,
            airplane=self.airplane,
        )

        self.ticket1 = Ticket.objects.create(
            flight=self.flight,
            passenger_name="John Doe",
            row=5,
            seat="A",
            status="booked",
        )
        self.ticket2 = Ticket.objects.create(
            flight=self.flight,
            passenger_name="Jane Doe",
            row=5,
            seat="B",
            status="booked",
        )

        self.order = Order.objects.create(
            user=self.user, total_price=Decimal("299.98"), status="pending"
        )
        self.order.tickets.add(self.ticket1, self.ticket2)

    def test_string_representation(self):
        """Test the order string representation"""
        expected = f"Order #{self.order.pk} by {self.user}"
        self.assertEqual(str(self.order), expected)

    def test_order_tickets_relationship(self):
        """Test the relationship between Order and Tickets"""
        self.assertEqual(self.order.tickets.count(), 2)
        self.assertIn(self.ticket1, self.order.tickets.all())
        self.assertIn(self.ticket2, self.order.tickets.all())


class OrderAPITest(APITestCase):
    """Tests for the Order API endpoints"""

    def setUp(self):

        self.user = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="password123",
        )
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="admin123",
            is_staff=True,
        )

        self.source_airport = Airport.objects.create(
            name="SFO Airport", closest_big_city="San Francisco"
        )
        self.destination_airport = Airport.objects.create(
            name="SEA Airport", closest_big_city="Seattle"
        )
        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.destination_airport,
            distance=1200,
        )
        self.airplane_type = AirplaneType.objects.create(
            name="Airbus A320", rows=25, seats_in_row=6
        )
        self.airplane = Airplane.objects.create(
            name="SG-2001", airplane_type=self.airplane_type
        )

        now = timezone.now()
        self.flight = Flight.objects.create(
            flight_number="SG456",
            departure_time=now + timedelta(days=7),
            arrival_time=now + timedelta(days=7, hours=2),
            route=self.route,
            airplane=self.airplane,
        )

        self.ticket = Ticket.objects.create(
            flight=self.flight,
            passenger_name="Alex Smith",
            row=10,
            seat="C",
            status="booked",
        )

        self.order = Order.objects.create(
            user=self.user, total_price=Decimal("149.99"), status="pending"
        )
        self.order.tickets.add(self.ticket)

        self.client = APIClient()
        self.orders_url = "/api/orders/"
        self.order_detail_url = f"{self.orders_url}{self.order.id}/"
        self.cancel_url = f"{self.order_detail_url}cancel/"

    def test_get_orders_requires_authentication(self):
        """Test that authentication is required to access orders"""
        response = self.client.get(self.orders_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_view_own_orders(self):
        """Test that a user can view their own orders"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.orders_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.order.id)

    def test_user_cannot_view_others_orders(self):
        """Test that a user cannot view orders of other users"""

        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="otherpass",
        )
        other_order = Order.objects.create(
            user=other_user, total_price=Decimal("99.99"), status="pending"
        )

        self.client.force_authenticate(user=self.user)

        other_order_url = f"{self.orders_url}{other_order.id}/"
        response = self.client.get(other_order_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cancel_order(self):
        """Test cancelling an order"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.cancel_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "canceled")

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, "canceled")
