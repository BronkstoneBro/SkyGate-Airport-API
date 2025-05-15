from rest_framework import serializers
from .models import Order
from tickets.serializers import TicketSerializer


ACTIVE_ORDER_STATUSES = ["paid", "processing"]


class OrderSerializer(serializers.ModelSerializer):
    tickets_details = TicketSerializer(
        source="tickets", many=True, read_only=True
    )
    user_email = serializers.EmailField(source="user.email", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "user_email",
            "username",
            "tickets",
            "tickets_details",
            "total_price",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]

    def validate_tickets(self, tickets):
        """
        Ensure that no selected ticket is already associated with an active order.
        """
        if tickets:
            for ticket in tickets:
                if Order.objects.filter(
                    tickets=ticket, status__in=ACTIVE_ORDER_STATUSES
                ).exists():
                    raise serializers.ValidationError(
                        f"Ticket {ticket.id} is already part of an active order."
                    )
        return tickets

    def validate(self, data):
        """
        General order validation:
        - At least one ticket must be included when creating an order.
        - Total price must be positive if explicitly provided.
        """
        tickets = data.get("tickets") or getattr(
            self.instance, "tickets", None
        )
        total_price = data.get("total_price")

        if not tickets and not self.instance:
            raise serializers.ValidationError(
                {"tickets": "At least one ticket is required for a new order."}
            )

        if total_price is not None and total_price <= 0:
            raise serializers.ValidationError(
                {"total_price": "Total price must be greater than zero."}
            )

        return data

    def create(self, validated_data):
        """
        Optionally calculate total price automatically instead of trusting client input.
        """
        tickets = validated_data.get("tickets", [])
        if tickets and "total_price" not in validated_data:
            validated_data["total_price"] = sum(
                ticket.price for ticket in tickets
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Optionally recalculate total_price if tickets are updated.
        """
        tickets = validated_data.get("tickets")
        if tickets is not None:
            validated_data["total_price"] = sum(
                ticket.price for ticket in tickets
            )
        return super().update(instance, validated_data)
