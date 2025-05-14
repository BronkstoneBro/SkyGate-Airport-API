from django.contrib import admin
from tickets.models import Ticket
from django import forms


class TicketAdminForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = "__all__"


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    form = TicketAdminForm
    list_display = ("id", "flight", "passenger_name", "get_seat", "status")
    search_fields = ("flight__flight_number", "passenger_name")
    ordering = ("flight", "row", "seat")
    readonly_fields = ("get_available_seats",)

    def get_seat(self, obj):
        """Return a combined seat representation."""
        return f"{obj.row}{obj.seat}"

    get_seat.short_description = "Seat"

    def get_available_seats(self, obj):
        """Simplified display of available seats."""
        if not obj.flight:
            return "Select a flight first to see available seats"

        airplane_type = obj.flight.airplane.airplane_type
        total_rows = airplane_type.rows
        seats_per_row = airplane_type.seats_in_row
        booked_seats = Ticket.objects.filter(
            flight=obj.flight, status__in=["booked", "checked_in"]
        ).exclude(pk=obj.pk)

        booked_set = {f"{t.row}{t.seat}" for t in booked_seats}
        available_seats = total_rows * seats_per_row - len(booked_set)

        return f"Available seats: {available_seats}"

    get_available_seats.short_description = "Available Seats"

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {"fields": ("flight", "passenger_name", "status")}),
            (
                "Seat Information",
                {
                    "fields": ("row", "seat", "get_available_seats"),
                    "description": "Select a valid seat for this flight",
                },
            ),
        )
