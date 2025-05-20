from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from orders.models import Order
from orders.serializers import OrderSerializer
from orders.schemas import list_orders_schema, create_order_schema, cancel_order_schema
from skygate_airport_api.permissions import IsOwnerOrReadOnly


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing orders.

    - Regular users can view and modify only their orders.
    - Admin users have full access.
    """

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "created_at"]
    ordering_fields = ["created_at", "total_price"]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
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

    def can_cancel(self, order):
        return order.status == "pending"

    @cancel_order_schema
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()

        if not self.can_cancel(order):
            return Response(
                {"error": "Only pending orders can be canceled"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = "canceled"
        order.save()

        order.tickets.update(status="canceled")

        return Response(
            {"status": "Order canceled successfully"},
            status=status.HTTP_200_OK,
        )
