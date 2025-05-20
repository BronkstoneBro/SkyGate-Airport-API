from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(generics.CreateAPIView):
    """
    Register a new user account.

    This endpoint allows new users to register by providing their credentials and basic information.
    """

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_description="Create a new user account with username, email, password, and profile details",
        responses={
            201: RegisterSerializer,
            400: "Bad request (validation error)",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserDetailView(generics.RetrieveAPIView):
    """
    Retrieve authenticated user details.

    This endpoint returns the profile information of the currently authenticated user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Get the current user's profile information",
        responses={
            200: UserSerializer,
            401: "Authentication credentials were not provided",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """
    Logout the current user.

    This endpoint allows users to logout, effectively invalidating their current token.
    """

    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Logout the current user session",
        responses={
            200: openapi.Response(
                description="Successfully logged out",
                examples={
                    "application/json": {"message": "Successfully logged out."}
                },
            ),
            401: "Authentication credentials were not provided",
        },
    )
    def post(self, request):
        return Response(
            {"message": "Successfully logged out."}, status=status.HTTP_200_OK
        )
