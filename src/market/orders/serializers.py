from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'pk',
            'cost',
            'delivery_city',
            'delivery_address',
            'delivery_method',
            'payment_method',
        )
