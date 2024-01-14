from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.views.decorators.http import require_POST
from market.products.models import Product
from market.sellers.models import SellerProduct
from .cart import Cart

# Create your views here.
def cart_remove(request: HttpRequest, product_id: str):
    cart = Cart(request)
    cart.remove(product_id=product_id)
    return redirect(reverse('cart:cart_detail'))


def cart_detail(request: HttpRequest):
    return render(request, 'cart/cart.html')




        
