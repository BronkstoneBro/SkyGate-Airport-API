"""
URL configuration for skygate_airport_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView

from airports.views import AirportViewSet, RouteViewSet
from airplanes.views import AirplaneViewSet, AirplaneTypeViewSet
from flights.views import FlightViewSet, CrewViewSet
from tickets.views import TicketViewSet
from orders.views import OrderViewSet
from authentication.views import RegisterView, UserDetailView, LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

api_router = DefaultRouter()


api_router.register(r"airports", AirportViewSet, basename="airport")
api_router.register(r"airports/routes", RouteViewSet, basename="route")
api_router.register(r"airplanes", AirplaneViewSet, basename="airplane")
api_router.register(
    r"airplanes/types", AirplaneTypeViewSet, basename="airplanetype"
)
api_router.register(r"flights", FlightViewSet, basename="flight")
api_router.register(r"flights/crew", CrewViewSet, basename="crew")
api_router.register(r"tickets", TicketViewSet, basename="ticket")
api_router.register(r"orders", OrderViewSet, basename="order")

schema_view = get_schema_view(
    openapi.Info(
        title="SkyGate Airport API",
        default_version="v1",
        description="A comprehensive API for managing airport operations including flights, tickets, airports, and airplanes.",
        terms_of_service="https://www.skygate-airport.com/terms/",
        contact=openapi.Contact(email="contact@skygate-airport.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/api/", permanent=False), name="index"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
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
    path("api/", include(api_router.urls)),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path(
        "api/auth/login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/auth/login/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("api/auth/logout/", LogoutView.as_view(), name="logout"),
    path("api/auth/me/", UserDetailView.as_view(), name="user_details"),
    path("api/auth/", include("authentication.urls")),
    path("api/airports/", include("airports.urls")),
    path("api/airplanes/", include("airplanes.urls")),
    path("api/flights/", include("flights.urls")),
    path("api/tickets/", include("tickets.urls")),
    path("api/orders/", include("orders.urls")),
]
