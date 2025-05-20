from rest_framework import serializers
from airplanes.models import Airplane, AirplaneType


class AirplaneTypeSerializer(serializers.ModelSerializer):
    total_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = AirplaneType
        fields = ["id", "name", "rows", "seats_in_row", "total_seats"]


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = AirplaneTypeSerializer(read_only=True)
    airplane_type_id = serializers.PrimaryKeyRelatedField(
        queryset=AirplaneType.objects.all(),
        source="airplane_type",
        write_only=True,
    )

    class Meta:
        model = Airplane
        fields = ["id", "name", "airplane_type", "airplane_type_id"]
