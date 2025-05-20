from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from orders.models import Order
from orders.serializers import OrderSerializer
from orders.schemas import (
    list_orders_schema,
    create_order_schema,
    cancel_order_schema,
)
from orders.permissions import IsOrderOwner


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing orders.

    Users can view and modify only their own orders.
    Admins have access to all orders.
    """

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "created_at"]
    ordering_fields = ["created_at", "total_price"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()

        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @list_orders_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @create_order_schema
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @cancel_order_schema
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status != "pending":
            return Response(
                {"error": "Only pending orders can be cancelled"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = "cancelled"
        order.save()

        # Cancel all tickets in the order
        for ticket in order.tickets.all():
            ticket.status = "cancelled"
            ticket.save()

        return Response({"status": "Order cancelled successfully"})
