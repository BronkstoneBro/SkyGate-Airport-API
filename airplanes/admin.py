from django.contrib import admin
from airplanes.models import Airplane, AirplaneType


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_rows", "get_seats_in_row")
    search_fields = ("name",)
    ordering = ("name",)
    
    def get_rows(self, obj):
        return obj.airplane_type.rows
    get_rows.short_description = "Rows"
    
    def get_seats_in_row(self, obj):
        return obj.airplane_type.seats_in_row
    get_seats_in_row.short_description = "Seats In Row"


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rows", "seats_in_row", "total_seats")
    search_fields = ("name",)
