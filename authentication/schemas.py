from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from functools import wraps


register_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=[
        "username",
        "password",
        "password2",
        "email",
        "first_name",
        "last_name",
    ],
    properties={
        "username": openapi.Schema(
            type=openapi.TYPE_STRING, description="Username"
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING, description="Password"
        ),
        "password2": openapi.Schema(
            type=openapi.TYPE_STRING, description="Password confirmation"
        ),
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
            format="email",
            description="Email address",
        ),
        "first_name": openapi.Schema(
            type=openapi.TYPE_STRING, description="First name"
        ),
        "last_name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Last name"
        ),
    },
)

user_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="User ID"),
        "username": openapi.Schema(
            type=openapi.TYPE_STRING, description="Username"
        ),
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
            format="email",
            description="Email address",
        ),
        "first_name": openapi.Schema(
            type=openapi.TYPE_STRING, description="First name"
        ),
        "last_name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Last name"
        ),
    },
)

logout_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "message": openapi.Schema(
            type=openapi.TYPE_STRING, description="Logout message"
        ),
    },
)

error_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "error": openapi.Schema(
            type=openapi.TYPE_STRING, description="Error message"
        ),
    },
)


def register_view_schema(func):
    @wraps(func)
    @swagger_auto_schema(
        operation_description="Create a new user account with username, email, password, and profile details",
        request_body=register_schema,
        responses={
            201: register_schema,
            400: error_response_schema,
        },
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def user_detail_view_schema(func):
    @wraps(func)
    @swagger_auto_schema(
        operation_description="Get the current user's profile information",
        responses={
            200: user_schema,
            401: error_response_schema,
        },
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def logout_view_schema(func):
    @wraps(func)
    @swagger_auto_schema(
        operation_description="Logout the current user session",
        responses={
            200: logout_response_schema,
            401: error_response_schema,
        },
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
