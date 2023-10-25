from django.shortcuts import render
from django.views.generic import DetailView, ListView

from market.categories.mixins import MenuMixin
from market.products.models import Product


class ProductDetailView(MenuMixin, DetailView):
    template_name = 'products/product_details.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
