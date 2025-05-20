from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import OrderSerializer


list_orders_schema = swagger_auto_schema(
    operation_description="List orders. Users see their own; admins see all.",
    responses={
        200: OrderSerializer(many=True),
        401: "Authentication required",
    },
)


create_order_schema = swagger_auto_schema(
    operation_description="Create a new order. Authenticated user is set as owner.",
    responses={
        201: OrderSerializer,
        400: "Validation error",
        401: "Authentication required",
    },
)


cancel_order_schema = swagger_auto_schema(
    operation_description="Cancel an order and its tickets. Only owner can cancel.",
    responses={
        200: openapi.Response(
            description="Order canceled successfully",
            examples={
                "application/json": {"status": "Order canceled successfully"}
            },
        ),
        400: "Only pending orders can be canceled",
        401: "Authentication required",
        403: "Permission denied",
        404: "Order not found",
    },
)
