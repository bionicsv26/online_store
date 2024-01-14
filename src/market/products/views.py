from typing import Any
from django.db.models import Min
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from market.categories.mixins import MenuMixin
from market.products.models import Product
from market.sellers.models import SellerProduct
from market.cart.cart import Cart


class ProductDetailView(MenuMixin, DetailView):
    template_name = 'products/product_details.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().prefetch_related('seller_products')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        response = super().get(request, *args, **kwargs)
        cart = Cart(request)
        amount = request.GET.get('amount')
        seller_product_id = request.GET.get('seller_product_pk')

        if seller_product_id is None:
            product = self.model.objects.get(slug=kwargs['product_slug'])
            seller_product = product.seller_products.order_by('price').first()
        else:
            seller_product = SellerProduct.objects.get(id=seller_product_id)
            amount = 1

        if amount or seller_product_id:
            cart.add(seller_product, amount)

        return response
