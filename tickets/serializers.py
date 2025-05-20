from rest_framework import serializers
from tickets.models import Ticket
import string
from django.core.exceptions import ValidationError
from flights.serializers import FlightSerializer


class TicketSerializer(serializers.ModelSerializer):
    flight_details = FlightSerializer(source="flight", read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "flight",
            "flight_details",
            "passenger_name",
            "row",
            "seat",
            "status",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        ticket = Ticket(**data)
        try:
            ticket.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        flight = data.get("flight")
        row = data.get("row")
        seat = data.get("seat")

        if flight and row and seat:
            existing_ticket = Ticket.objects.filter(
                flight=flight,
                row=row,
                seat=seat.upper(),
                status__in=["booked", "checked_in"],
            ).first()

            if existing_ticket:
                raise serializers.ValidationError(
                    {
                        "seat": f"Seat {row}{seat.upper()} is already booked on this flight."
                    }
                )

        return data

    def validate_seat(self, value):
        if not value or len(value) != 1:
            raise serializers.ValidationError(
                "Seat must be a single character."
            )
        if value not in string.ascii_letters:
            raise serializers.ValidationError("Seat must be a letter.")
        return value.upper()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["seat_code"] = f"{instance.row}{instance.seat}"

        return representation
