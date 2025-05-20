from django.test import TestCase
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from flights.models import Flight, Crew

from airports.models import Airport, Route
from airplanes.models import Airplane, AirplaneType


class CrewModelTest(TestCase):
    """Tests for the Crew model"""

    def setUp(self):
        self.crew_member = Crew.objects.create(
            first_name="John", last_name="Smith", role="Pilot"
        )

    def test_string_representation(self):
        """Test the string representation of a crew member"""
        self.assertEqual(str(self.crew_member), "John Smith (Pilot)")


class FlightModelTest(TestCase):
    """Tests for the Flight model"""

    def setUp(self):

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

        self.pilot = Crew.objects.create(
            first_name="John", last_name="Smith", role="Pilot"
        )
        self.co_pilot = Crew.objects.create(
            first_name="Jane", last_name="Doe", role="Co-Pilot"
        )

        # Create flight
        now = timezone.now()
        self.flight = Flight.objects.create(
            flight_number="SG123",
            departure_time=now + timedelta(hours=2),
            arrival_time=now + timedelta(hours=6),
            route=self.route,
            airplane=self.airplane,
        )
        self.flight.crew.add(self.pilot, self.co_pilot)

    def test_string_representation(self):
        """Test the flight string representation"""
        expected = f"Flight SG123 ({self.route})"
        self.assertEqual(str(self.flight), expected)

    def test_arrival_before_departure_validation(self):
        """Test validation error when arrival time is before departure time"""
        now = timezone.now()

        with self.assertRaises(ValidationError):
            invalid_flight = Flight(
                flight_number="SG456",
                departure_time=now + timedelta(hours=4),
                arrival_time=now + timedelta(hours=2),  # Before departure time
                route=self.route,
                airplane=self.airplane,
            )
            invalid_flight.full_clean()

    def test_crew_relationship(self):
        """Test that crew members are correctly associated with a flight"""
        self.assertEqual(self.flight.crew.count(), 2)
        self.assertIn(self.pilot, self.flight.crew.all())
        self.assertIn(self.co_pilot, self.flight.crew.all())


class FlightAPITest(APITestCase):
    """Tests for the Flight API endpoints"""

    def setUp(self):
        self.client = APIClient()

        self.source_airport = Airport.objects.create(
            name="CDG Airport", closest_big_city="Paris"
        )
        self.destination_airport = Airport.objects.create(
            name="FCO Airport", closest_big_city="Rome"
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

        self.crew1 = Crew.objects.create(
            first_name="Alex", last_name="Johnson", role="Captain"
        )
        self.crew2 = Crew.objects.create(
            first_name="Maria", last_name="Garcia", role="Flight Attendant"
        )

        now = timezone.now()
        self.flight = Flight.objects.create(
            flight_number="SG789",
            departure_time=now + timedelta(days=1),
            arrival_time=now + timedelta(days=1, hours=3),
            route=self.route,
            airplane=self.airplane,
        )
        self.flight.crew.add(self.crew1, self.crew2)

        self.flights_url = "/api/flights/"
        self.flight_detail_url = f"{self.flights_url}{self.flight.id}/"

    def test_get_flights_list(self):
        """Test retrieving the list of flights"""
        response = self.client.get(self.flights_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["flight_number"], "SG789")

    def test_get_flight_detail(self):
        """Test retrieving a specific flight"""
        response = self.client.get(self.flight_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["flight_number"], "SG789")
