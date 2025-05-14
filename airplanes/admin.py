from django.contrib import admin
from airplanes.models import Airplane


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rows", "seats_in_row")
    search_fields = ("name",)
    ordering = ("name",)
