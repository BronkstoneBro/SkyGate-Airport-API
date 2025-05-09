from django.db import models


class AirplaneType(models.Model):
    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    @property
    def total_seats(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name} ({self.total_seats} seats)"


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    airplane_type = models.ForeignKey(
        AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )

    def __str__(self):
        return f"{self.name} - {self.airplane_type.name}"
