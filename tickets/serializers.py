from rest_framework import serializers
from .models import Ticket
import string
from django.core.exceptions import ValidationError


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

    def validate(self, data):
        ticket = Ticket(**data)
        try:
            ticket.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return data

    def validate_seat(self, value):
        if not value or len(value) != 1:
            raise serializers.ValidationError(
                "Seat must be a single character."
            )
        if value not in string.ascii_letters:
            raise serializers.ValidationError("Seat must be a letter.")
        return value.upper()
