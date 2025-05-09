from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AirplaneViewSet, AirplaneTypeViewSet

router = DefaultRouter()
router.register(r"types", AirplaneTypeViewSet)
router.register(r"airplanes", AirplaneViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
