from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


token_obtain_pair_schema = swagger_auto_schema(
    operation_description="Obtain JWT token pair (access and refresh tokens)",
    responses={
        200: openapi.Response(
            description="Token pair obtained successfully",
            examples={
                "application/json": {
                    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                }
            },
        ),
        401: "Invalid credentials",
    },
)


token_refresh_schema = swagger_auto_schema(
    operation_description="Refresh JWT access token using refresh token",
    responses={
        200: openapi.Response(
            description="Access token refreshed successfully",
            examples={
                "application/json": {
                    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                }
            },
        ),
        401: "Invalid or expired refresh token",
    },
)


token_verify_schema = swagger_auto_schema(
    operation_description="Verify JWT token validity",
    responses={
        200: openapi.Response(
            description="Token is valid", examples={"application/json": {}}
        ),
        401: "Invalid token",
    },
)
