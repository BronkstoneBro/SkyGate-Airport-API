from django.db import models
from flights.models import Flight


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

    def __str__(self):
        return f"{self.passenger_name} - Seat {self.row}{self.seat} on flight {self.flight.flight_number}"
