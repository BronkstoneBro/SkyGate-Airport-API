from django.db import models
from airplanes.models import Airplane
from airports.models import Route
from django.core.exceptions import ValidationError


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane, on_delete=models.CASCADE, related_name="flights"
    )
    crew = models.ManyToManyField(Crew, related_name="flights")

    def __str__(self):
        return f"Flight {self.flight_number} ({self.route})"

    def clean(self):

        if self.arrival_time <= self.departure_time:
            raise ValidationError("Arrival time must be after departure time")

        overlapping_flights = Flight.objects.filter(
            airplane=self.airplane,
            departure_time__lt=self.arrival_time,
            arrival_time__gt=self.departure_time,
        ).exclude(pk=self.pk)

        if overlapping_flights.exists():
            raise ValidationError(
                "This airplane is already scheduled for another flight during this time"
            )

        if Flight.objects.filter(
            flight_number=self.flight_number, route=self.route
        ).exists():
            raise ValidationError(
                f"Flight number {self.flight_number} already exists on this route"
            )

        if self.airplane.capacity < self.route.minimum_capacity:
            raise ValidationError(
                f"Airplane capacity {self.airplane.capacity} is less than the minimum capacity required for this route"
            )
