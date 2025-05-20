from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from authentication.schemas import (
    register_view_schema,
    user_detail_view_schema,
    logout_view_schema,
)


class RegisterView(generics.CreateAPIView):
    """
    Register a new user account.

    This endpoint allows new users to register by providing their credentials and basic information.
    """

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    @register_view_schema
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

    @user_detail_view_schema
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

    @logout_view_schema
    def post(self, request):
        return Response(
            {"message": "Successfully logged out."}, status=status.HTTP_200_OK
        )
