from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from market.categories.mixins import MenuMixin
from market.products.models import Product
from market.cart.cart import Cart


class ProductDetailView(MenuMixin, DetailView):
    template_name = 'products/product_details.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_queryset(self) -> QuerySet[Any]:
        return Product.objects.prefetch_related('seller_products')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        amount = request.GET.get('amount')
        cart = Cart(request)
        
        return super().get(request, *args, **kwargs)
