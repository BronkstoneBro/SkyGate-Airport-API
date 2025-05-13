from rest_framework import serializers
from .models import Crew, Flight


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class FlightSerializer(serializers.ModelSerializer):
    crew = CrewSerializer(many=True, read_only=True)
    crew_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Crew.objects.all(), write_only=True, source="crew"
    )

    class Meta:
        model = Flight
        fields = [
            "id",
            "flight_number",
            "departure_time",
            "arrival_time",
            "route",
            "airplane",
            "crew",
            "crew_ids",
        ]
