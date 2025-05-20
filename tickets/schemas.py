from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import TicketSerializer


create_ticket_schema = swagger_auto_schema(
    operation_description="Create a new ticket. Users can only create tickets for themselves.",
    responses={
        201: TicketSerializer,
        400: "Bad request",
        403: "Forbidden",
    },
)


update_ticket_schema = swagger_auto_schema(
    operation_description="Update a ticket. Users can only update their tickets.",
    responses={
        200: TicketSerializer,
        400: "Bad request",
        403: "Forbidden",
        404: "Not found",
    },
)


available_seats_schema = swagger_auto_schema(
    operation_description="Get available seats for a flight",
    responses={
        200: openapi.Response(
            description="Available seats info",
            examples={
                "application/json": {
                    "flight_id": 1,
                    "flight_number": "FL123",
                    "total_seats": 100,
                    "booked_seats": 50,
                    "available_seats": 50,
                    "seats": [
                        {"row": 1, "seat": "A", "seat_code": "1A"},
                        {"row": 1, "seat": "B", "seat_code": "1B"},
                    ],
                }
            },
        ),
        404: "Flight not found",
    },
)
