from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.http import HttpRequest, HttpResponse
from .cart import Cart
from market.products.models import Product

# Create your views here.
class CartDetailsView(TemplateView):
    template_name = 'cart/cart.html'


class CartAddView(View):
    
    def get(self, request:HttpRequest, product_id: str) -> HttpResponse:
        cart = Cart(request.session)
        product = get_object_or_404(Product, pk=int(product_id))
        seller_product = product.seller_products.order_by('price').first()

        cart.add(seller_product, amount=1)
        return redirect(reverse('market.catalog_app:catalog'))
    

class CartRemoveView(View):

    def get(self, request: HttpRequest, product_id: str) -> HttpResponse:
        cart = Cart(request.session)
        cart.remove(product_id=product_id)
        return redirect(reverse('market.cart:cart_details'))
