from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .cart import Cart

# Create your views here.
def cart_remove(request: HttpRequest, product_id: str):
    cart = Cart(request)
    cart.remove(product_id=product_id)
    return redirect(reverse('cart:cart_detail'))


def cart_detail(request: HttpRequest):
    return render(request, 'cart/cart.html')




        
