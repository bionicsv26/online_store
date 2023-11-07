from django.shortcuts import render
from django.views.generic import DetailView

from rest_framework.viewsets import ModelViewSet
from .models import Order
from .serializers import OrderSerializer


class OrderDetailsView(DetailView):
    template_name = 'orders/order_details.html'
    queryset = Order.objects.prefetch_related('products')
    context_object_name = 'order'


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
