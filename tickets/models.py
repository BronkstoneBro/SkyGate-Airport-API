from django.db import models
from flights.models import Flight
from django.core.exceptions import ValidationError
import string


class Ticket(models.Model):
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="tickets"
    )
    passenger_name = models.CharField(max_length=100)
    row = models.PositiveIntegerField()
    seat = models.CharField(max_length=1)
    status = models.CharField(
        max_length=20,
        choices=[
            ("booked", "Booked"),
            ("canceled", "Canceled"),
            ("checked_in", "Checked In"),
        ],
        default="booked",
    )

    class Meta:
        unique_together = ("flight", "row", "seat")

    def clean(self):
        super().clean()

        if not self.flight:
            return

        airplane = self.flight.airplane
        airplane_type = airplane.airplane_type

        if self.row <= 0 or self.row > airplane_type.rows:
            raise ValidationError(
                {
                    "row": f"Row must be between 1 and {airplane_type.rows} for this airplane type."
                }
            )

        valid_seats = string.ascii_uppercase[: airplane_type.seats_in_row]
        if self.seat.upper() not in valid_seats:
            raise ValidationError(
                {
                    "seat": f"Seat must be one of {', '.join(valid_seats)} for this airplane type."
                }
            )

    def __str__(self):
        return f"{self.passenger_name} - Seat {self.row}{self.seat} on flight {self.flight.flight_number}"
