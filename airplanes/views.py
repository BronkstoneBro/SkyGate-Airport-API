from rest_framework import viewsets
from airplanes.models import Airplane, AirplaneType
from airplanes.serializers import AirplaneSerializer, AirplaneTypeSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
