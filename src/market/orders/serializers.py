from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = 'pk', 'seller_products', 'cost', 'comment', 'delivery_address'
