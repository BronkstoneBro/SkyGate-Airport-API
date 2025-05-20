from django.urls import path, include
from rest_framework.routers import DefaultRouter
from airplanes.views import AirplaneViewSet, AirplaneTypeViewSet

router = DefaultRouter()
router.register(r"types", AirplaneTypeViewSet, basename="airplanetype")
router.register(r"airplanes", AirplaneViewSet, basename="airplane")

urlpatterns = [
    path("", include(router.urls)),
]
