from rest_framework import serializers
from .models import Order
from tickets.models import Ticket


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
