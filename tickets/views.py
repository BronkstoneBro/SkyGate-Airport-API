from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Ticket
from .serializers import TicketSerializer
from flights.models import Flight


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_flight_or_404(self, flight_id):
        """Helper method to get a flight or return a 404 error."""
        try:
            return Flight.objects.get(pk=flight_id)
        except Flight.DoesNotExist:
            return None

    @action(
        detail=False,
        methods=["get"],
        url_path="available-seats/(?P<flight_id>[^/.]+)",
    )
    def available_seats(self, request, flight_id=None):
        """
        Return available seats for a specific flight
        """
        flight = self.get_flight_or_404(flight_id)

        if not flight:
            return Response(
                {"error": "Flight not found"}, status=status.HTTP_404_NOT_FOUND
            )

        airplane_type = flight.airplane.airplane_type
        total_rows = airplane_type.rows
        seats_per_row = airplane_type.seats_in_row

        booked_seats = Ticket.objects.filter(
            flight=flight, status__in=["booked", "checked_in"]
        ).values_list("row", "seat")

        booked_set = {f"{row}{seat}" for row, seat in booked_seats}

        available_seats = [
            {"row": row, "seat": seat, "seat_code": f"{row}{seat}"}
            for row in range(1, total_rows + 1)
            for seat in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:seats_per_row]
            if f"{row}{seat}" not in booked_set
        ]

        return Response(
            {
                "flight_id": flight_id,
                "flight_number": flight.flight_number,
                "total_seats": total_rows * seats_per_row,
                "booked_seats": len(booked_set),
                "available_seats": len(available_seats),
                "seats": available_seats,
            }
        )
