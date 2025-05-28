from django.contrib import admin
from flights.models import Flight, Crew


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "flight_number",
        "airplane",
        "route",
        "departure_time",
        "arrival_time",
    )
    list_filter = ("departure_time",)
    search_fields = (
        "flight_number",
        "airplane__name",
        "route__source__name",
        "route__destination__name",
    )
    ordering = ("-departure_time",)


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "role")
    search_fields = ("first_name", "last_name", "role")
    list_filter = ("role",)
    ordering = ("last_name",)
