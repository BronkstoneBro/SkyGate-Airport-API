from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AirportViewSet, RouteViewSet

router = DefaultRouter()

router.register(r"airports", AirportViewSet, basename="airport")
router.register(r"routes", RouteViewSet, basename="route")

urlpatterns = [
    path("", include(router.urls)),
]
