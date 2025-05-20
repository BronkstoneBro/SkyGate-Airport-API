"""
URL configuration for skygate_airport_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .schemas import (
    token_obtain_pair_schema,
    token_refresh_schema,
    token_verify_schema,
)

from airports.views import AirportViewSet, RouteViewSet
from airplanes.views import AirplaneViewSet, AirplaneTypeViewSet
from authentication.views import RegisterView, UserDetailView, LogoutView
from flights.views import FlightViewSet, CrewViewSet
from tickets.views import TicketViewSet
from orders.views import OrderViewSet


# Swagger / ReDoc schema
schema_view = get_schema_view(
    openapi.Info(
        title="SkyGate Airport API",
        default_version="v1",
        description="API for SkyGate Airport management system",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@skygate.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# Router registration
api_router = DefaultRouter()
api_router.register(
    r"airports",
    AirportViewSet,
    basename="airport",
)
api_router.register(
    r"airports/routes",
    RouteViewSet,
    basename="route",
)
api_router.register(
    r"airplanes",
    AirplaneViewSet,
    basename="airplane",
)
api_router.register(
    r"airplanes/types",
    AirplaneTypeViewSet,
    basename="airplanetype",
)
api_router.register(
    r"flights",
    FlightViewSet,
    basename="flight",
)
api_router.register(
    r"flights/crew",
    CrewViewSet,
    basename="crew",
)
api_router.register(
    r"tickets",
    TicketViewSet,
    basename="ticket",
)
api_router.register(
    r"orders",
    OrderViewSet,
    basename="order",
)


# URL patterns
urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "",
        RedirectView.as_view(url="/api/", permanent=False),
        name="index",
    ),
    path(
        "api/",
        include(api_router.urls),
    ),
    path(
        "api/auth/register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "api/auth/logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "api/auth/me/",
        UserDetailView.as_view(),
        name="user_details",
    ),
    path(
        "api/auth/",
        include("authentication.urls"),
    ),
    path(
        "api/token/",
        token_obtain_pair_schema(TokenObtainPairView.as_view()),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        token_refresh_schema(TokenRefreshView.as_view()),
        name="token_refresh",
    ),
    path(
        "api/token/verify/",
        token_verify_schema(TokenVerifyView.as_view()),
        name="token_verify",
    ),
    path(
        "api/airports/",
        include("airports.urls"),
    ),
    path(
        "api/airplanes/",
        include("airplanes.urls"),
    ),
    path(
        "api/flights/",
        include("flights.urls"),
    ),
    path(
        "api/tickets/",
        include("tickets.urls"),
    ),
    path(
        "api/orders/",
        include("orders.urls"),
    ),
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
