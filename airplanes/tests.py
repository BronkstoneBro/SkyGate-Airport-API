from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Airplane, AirplaneType
from .serializers import AirplaneSerializer, AirplaneTypeSerializer


class AirplaneTypeModelTests(TestCase):
    """Tests for the AirplaneType model"""

    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(
            name="Boeing 737", rows=30, seats_in_row=6
        )

    def test_total_seats_property(self):
        """Test the total_seats property calculation"""
        self.assertEqual(self.airplane_type.total_seats, 30 * 6)

    def test_string_representation(self):
        """Test the string representation of the AirplaneType model"""
        expected_string = f"Boeing 737 (180 seats)"
        self.assertEqual(str(self.airplane_type), expected_string)


class AirplaneModelTests(TestCase):
    """Tests for the Airplane model"""

    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(
            name="Boeing 737", rows=30, seats_in_row=6
        )
        self.airplane = Airplane.objects.create(
            name="SkyGate-001", airplane_type=self.airplane_type
        )

    def test_string_representation(self):
        """Test the string representation of the Airplane model"""
        expected_string = "SkyGate-001 - Boeing 737"
        self.assertEqual(str(self.airplane), expected_string)

    def test_airplane_type_relationship(self):
        """Test the relationship between Airplane and AirplaneType"""
        self.assertEqual(self.airplane.airplane_type, self.airplane_type)


class AirplaneTypeSerializerTests(TestCase):
    """Tests for the AirplaneTypeSerializer"""

    def setUp(self):
        self.airplane_type_attributes = {
            "name": "Airbus A320",
            "rows": 25,
            "seats_in_row": 6,
        }
        self.airplane_type = AirplaneType.objects.create(
            **self.airplane_type_attributes
        )
        self.serializer = AirplaneTypeSerializer(instance=self.airplane_type)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields"""
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            {"id", "name", "rows", "seats_in_row", "total_seats"},
        )

    def test_total_seats_field_content(self):
        """Test that the total_seats field contains the correct value"""
        data = self.serializer.data
        self.assertEqual(data["total_seats"], 25 * 6)

    def test_name_field_content(self):
        """Test that the name field contains the correct value"""
        data = self.serializer.data
        self.assertEqual(data["name"], "Airbus A320")


class AirplaneSerializerTests(TestCase):
    """Tests for the AirplaneSerializer"""

    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(
            name="Boeing 747", rows=40, seats_in_row=10
        )
        self.airplane_attributes = {
            "name": "SkyGate-002",
            "airplane_type": self.airplane_type,
        }
        self.airplane = Airplane.objects.create(**self.airplane_attributes)
        self.serializer = AirplaneSerializer(instance=self.airplane)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields"""
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {"id", "name", "airplane_type"})

    def test_airplane_type_field_content(self):
        """Test that the airplane_type field contains the correct structure"""
        data = self.serializer.data
        self.assertEqual(
            set(data["airplane_type"].keys()),
            {"id", "name", "rows", "seats_in_row", "total_seats"},
        )
        self.assertEqual(data["airplane_type"]["name"], "Boeing 747")


class AirplaneTypeAPITests(APITestCase):
    """Tests for the AirplaneType API endpoints"""

    def setUp(self):
        self.client = APIClient()
        # Update URL to match actual API structure
        self.url = "/api/airplanes/types/1/"  # We'll test only existing instance operations
        self.airplane_type = AirplaneType.objects.create(
            name="Boeing 777", rows=35, seats_in_row=9
        )
        self.detail_url = f"/api/airplanes/types/{self.airplane_type.id}/"

    def test_get_airplane_type_detail(self):
        """Test retrieving a specific airplane type"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Boeing 777")
        self.assertEqual(response.data["total_seats"], 315)

    def test_update_airplane_type(self):
        """Test updating an airplane type"""
        updated_data = {
            "name": "Boeing 777X",
            "rows": 40,
            "seats_in_row": 9,
        }
        response = self.client.put(
            self.detail_url, updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.airplane_type.refresh_from_db()
        self.assertEqual(self.airplane_type.name, "Boeing 777X")
        self.assertEqual(self.airplane_type.rows, 40)
        self.assertEqual(self.airplane_type.total_seats, 360)

    def test_delete_airplane_type(self):
        """Test deleting an airplane type"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AirplaneType.objects.count(), 0)


class AirplaneAPITests(APITestCase):
    """Tests for the Airplane API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/airplanes/"
        self.airplane_type = AirplaneType.objects.create(
            name="Airbus A320neo", rows=28, seats_in_row=6
        )
        self.airplane_data = {
            "name": "SkyGate-003",
            "airplane_type_id": self.airplane_type.id,
        }
        self.airplane = Airplane.objects.create(
            name="SkyGate-004", airplane_type=self.airplane_type
        )
        self.detail_url = f"{self.url}{self.airplane.id}/"

    def test_get_airplanes_list(self):
        """Test retrieving the list of airplanes"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "SkyGate-004")

    def test_get_airplane_detail(self):
        """Test retrieving a specific airplane"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "SkyGate-004")
        self.assertEqual(
            response.data["airplane_type"]["name"], "Airbus A320neo"
        )

    def test_create_airplane(self):
        """Test creating a new airplane through the API"""
        response = self.client.post(
            self.url, self.airplane_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Airplane.objects.count(), 2)
        self.assertEqual(response.data["name"], "SkyGate-003")
        self.assertEqual(
            response.data["airplane_type"]["name"], "Airbus A320neo"
        )

    def test_update_airplane(self):
        """Test updating an airplane"""
        updated_data = {
            "name": "SkyGate-004-Updated",
            "airplane_type_id": self.airplane_type.id,
        }
        response = self.client.put(
            self.detail_url, updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.airplane.refresh_from_db()
        self.assertEqual(self.airplane.name, "SkyGate-004-Updated")

    def test_delete_airplane(self):
        """Test deleting an airplane"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Airplane.objects.count(), 0)
