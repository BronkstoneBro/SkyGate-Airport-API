from django.contrib import admin
from tickets.models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "flight", "seat", "price")
    list_filter = ("flight",)
    search_fields = ("flight__airplane__name", "seat")
    ordering = ("flight", "seat")
