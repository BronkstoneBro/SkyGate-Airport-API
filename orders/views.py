from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from orders.models import Order
from orders.serializers import OrderSerializer
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

    @swagger_auto_schema(
        operation_description="List orders. Users see their own; admins see all.",
        responses={
            200: OrderSerializer(many=True),
            401: "Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new order. Authenticated user is set as owner.",
        responses={
            201: OrderSerializer,
            400: "Validation error",
            401: "Authentication required",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def can_cancel(self, order):
        return order.status == "pending"

    @swagger_auto_schema(
        operation_description="Cancel an order and its tickets. Only owner can cancel.",
        responses={
            200: openapi.Response(
                description="Order canceled successfully",
                examples={
                    "application/json": {
                        "status": "Order canceled successfully"
                    }
                },
            ),
            400: "Only pending orders can be canceled",
            401: "Authentication required",
            403: "Permission denied",
            404: "Order not found",
        },
    )
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
