from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .cart import Cart
from market.products.models import Product

# Create your views here.
def cart_details(request: HttpRequest) -> HttpResponse:
    return render(request, 'cart/cart.html')


def cart_add(request: HttpRequest, product_id: str) -> HttpResponse:
    cart = Cart(request)
    product = get_object_or_404(Product, pk=int(product_id))
    seller_product = product.seller_products.order_by('price').first()

    cart.add(seller_product, amount=1)
    return redirect(reverse('market.catalog_app:catalog'))


def cart_remove(request: HttpRequest, product_id: str) -> HttpResponse:
    cart = Cart(request)
    cart.remove(product_id=product_id)
    return redirect(reverse('cart:cart_details'))