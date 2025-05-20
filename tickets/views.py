from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Ticket
from .serializers import TicketSerializer
from flights.models import Flight
from skygate_airport_api.permissions import (
    IsTicketOwner,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TicketViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing tickets.

    Users can view and modify only their own tickets.
    Admins have access to all tickets.
    """

    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsTicketOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["flight", "status"]
    ordering_fields = ["flight__departure_time", "passenger_name"]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Ticket.objects.none()
            
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        else:
            return Ticket.objects.filter(orders__user=user).distinct()

    def get_flight_or_404(self, flight_id):
        return get_object_or_404(Flight, pk=flight_id)

    def get_available_seats(self, flight):
        airplane_type = flight.airplane.airplane_type
        total_rows = airplane_type.rows
        seats_per_row = airplane_type.seats_in_row

        booked = Ticket.objects.filter(
            flight=flight, status__in=["booked", "checked_in"]
        ).values_list("row", "seat")

        booked_set = {f"{row}{seat}" for row, seat in booked}

        seats = [
            {"row": row, "seat": seat, "seat_code": f"{row}{seat}"}
            for row in range(1, total_rows + 1)
            for seat in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:seats_per_row]
            if f"{row}{seat}" not in booked_set
        ]

        return {
            "flight_id": flight.id,
            "flight_number": flight.flight_number,
            "total_seats": total_rows * seats_per_row,
            "booked_seats": len(booked_set),
            "available_seats": len(seats),
            "seats": seats,
        }

    @swagger_auto_schema(
        operation_description="Create a new ticket. Users can only create tickets for themselves.",
        responses={
            201: TicketSerializer,
            400: "Bad request",
            403: "Forbidden",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a ticket. Users can only update their tickets.",
        responses={
            200: TicketSerializer,
            400: "Bad request",
            403: "Forbidden",
            404: "Not found",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Get available seats for a flight",
        responses={
            200: openapi.Response(
                description="Available seats info",
            ),
            404: "Flight not found",
        },
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="available-seats/(?P<flight_id>[^/.]+)",
        permission_classes=[IsAuthenticated],
    )
    def available_seats(self, request, flight_id=None):
        flight = self.get_flight_or_404(flight_id)
        data = self.get_available_seats(flight)
        return Response(data)
