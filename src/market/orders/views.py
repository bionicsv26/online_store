from django.shortcuts import render
from django.views.generic import DetailView

from rest_framework.viewsets import ModelViewSet
from .models import Order
from .serializers import OrderSerializer


class OrderDetailsView(DetailView):
    template_name = 'orders/order_details.html'
    queryset = Order.objects.defer('created_at', 'status')
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seller_products'] = context['order'].seller_products.select_related('product').only('product__name')
        return context


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
