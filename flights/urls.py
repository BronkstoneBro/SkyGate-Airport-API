from django.urls import path, include
from rest_framework.routers import DefaultRouter
from flights.views import CrewViewSet, FlightViewSet

router = DefaultRouter()
router.register(r"crew", CrewViewSet, basename="crew")
router.register(r"flights", FlightViewSet, basename="flight")

urlpatterns = [
    path("", include(router.urls)),
]
