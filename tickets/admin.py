from django.contrib import admin
from tickets.models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "flight", "passenger_name", "get_seat", "status")
    list_filter = ("flight", "status")
    search_fields = ("flight__flight_number", "passenger_name")
    ordering = ("flight", "row", "seat")
    
    def get_seat(self, obj):
        return f"{obj.row}{obj.seat}"
    get_seat.short_description = "Seat"
