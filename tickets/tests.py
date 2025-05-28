from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.utils import timezone
from datetime import timedelta

from .models import Ticket
from flights.models import Flight, Crew
from airports.models import Airport, Route
from airplanes.models import Airplane, AirplaneType
from orders.models import Order


class TicketModelTest(TestCase):
    """Tests for the Ticket model"""

    def setUp(self):

        self.source_airport = Airport.objects.create(
            name="SIN Airport", closest_big_city="Singapore"
        )
        self.destination_airport = Airport.objects.create(
            name="HKG Airport", closest_big_city="Hong Kong"
        )
        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.destination_airport,
            distance=2500,
        )
        self.airplane_type = AirplaneType.objects.create(
            name="Boeing 777", rows=40, seats_in_row=8
        )
        self.airplane = Airplane.objects.create(
            name="SG-3001", airplane_type=self.airplane_type
        )

        now = timezone.now()
        self.flight = Flight.objects.create(
            flight_number="SG789",
            departure_time=now + timedelta(days=14),
            arrival_time=now + timedelta(days=14, hours=4),
            route=self.route,
            airplane=self.airplane,
        )

        self.ticket = Ticket.objects.create(
            flight=self.flight,
            passenger_name="Maria Garcia",
            row=15,
            seat="D",
            status="booked",
        )

    def test_string_representation(self):
        """Test the ticket string representation"""
        expected = f"Maria Garcia - Seat 15D on flight SG789"
        self.assertEqual(str(self.ticket), expected)

    def test_seat_validation(self):
        """Test validation for seat assignment"""

        with self.assertRaises(ValidationError):
            invalid_ticket = Ticket(
                flight=self.flight,
                passenger_name="Invalid Row",
                row=50,
                seat="A",
                status="booked",
            )
            invalid_ticket.full_clean()

        with self.assertRaises(ValidationError):
            invalid_ticket = Ticket(
                flight=self.flight,
                passenger_name="Invalid Seat",
                row=10,
                seat="Z",
                status="booked",
            )
            invalid_ticket.full_clean()


class TicketAPITest(APITestCase):
    """Tests for the Ticket API endpoints"""

    def setUp(self):

        self.user = User.objects.create_user(
            username="passenger",
            email="passenger@example.com",
            password="password123",
        )

        self.source_airport = Airport.objects.create(
            name="DXB Airport", closest_big_city="Dubai"
        )
        self.destination_airport = Airport.objects.create(
            name="DEL Airport", closest_big_city="Delhi"
        )
        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.destination_airport,
            distance=2200,
        )
        self.airplane_type = AirplaneType.objects.create(
            name="Airbus A380", rows=50, seats_in_row=10
        )
        self.airplane = Airplane.objects.create(
            name="SG-4001", airplane_type=self.airplane_type
        )

        now = timezone.now()
        self.flight = Flight.objects.create(
            flight_number="SG321",
            departure_time=now + timedelta(days=21),
            arrival_time=now + timedelta(days=21, hours=3, minutes=30),
            route=self.route,
            airplane=self.airplane,
        )

        self.ticket = Ticket.objects.create(
            flight=self.flight,
            passenger_name="James Wilson",
            row=20,
            seat="E",
            status="booked",
        )

        self.order = Order.objects.create(
            user=self.user, total_price=Decimal("299.99"), status="pending"
        )
        self.order.tickets.add(self.ticket)

        self.client = APIClient()
        self.tickets_url = "/api/tickets/"
        self.ticket_detail_url = f"{self.tickets_url}{self.ticket.id}/"

    def test_get_tickets_requires_authentication(self):
        """Test that authentication is required to access tickets"""
        response = self.client.get(self.tickets_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_view_own_tickets(self):
        """Test that a user can view tickets in their orders"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.tickets_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.ticket.id)
        self.assertEqual(response.data[0]["passenger_name"], "James Wilson")
        self.assertEqual(response.data[0]["seat_code"], "20E")

    def test_user_can_view_ticket_details(self):
        """Test that a user can view details of their ticket"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.ticket_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.ticket.id)
        self.assertEqual(response.data["passenger_name"], "James Wilson")
        self.assertEqual(response.data["status"], "booked")
        self.assertEqual(response.data["seat_code"], "20E")
        self.assertEqual(
            response.data["flight_details"]["flight_number"], "SG321"
        )

    def test_duplicate_seat_validation(self):
        """Test validation against booking already occupied seats"""
        self.client.force_authenticate(user=self.user)

        duplicate_seat_data = {
            "flight": self.flight.id,
            "passenger_name": "Duplicate Seat User",
            "row": 20,
            "seat": "E",
            "status": "booked",
        }
        response = self.client.post(
            self.tickets_url, duplicate_seat_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(
            "non_field_errors" in response.data or "seat" in response.data,
            "Expected validation error for duplicate seat",
        )
