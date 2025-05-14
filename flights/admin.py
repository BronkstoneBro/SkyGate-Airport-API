from django.contrib import admin
from flights.models import Flight
from flights.models import Route


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "airplane",
        "route",
        "departure_time",
        "arrival_time",
        "status",
    )
    list_filter = ("status", "departure_time")
    search_fields = (
        "airplane__name",
        "route__departure__name",
        "route__arrival__name",
    )
    ordering = ("-departure_time",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("id", "departure", "arrival")
    search_fields = ("departure__name", "arrival__name")
