from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.views.decorators.http import require_POST
from market.products.models import Product
from market.sellers.models import SellerProduct
from .cart import Cart

# Create your views here.
@require_POST
def change_amount(request: HttpRequest, product_id, amount):
    cart = Cart(request)
    product = get_object_or_404(SellerProduct, id=product_id)
    cart.change_amount(product=product,
                       amount=amount)
    return redirect


@require_POST
def cart_add(request: HttpRequest, product_id, amount):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    product = product.seller_products
    print(product)
    cart.add(product=product,
             amount=amount)
    return redirect('sellers:seller-details')


@require_POST
def cart_remove(request: HttpRequest, product_id):
    cart = Cart(request)
    product = get_object_or_404(SellerProduct, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail') # Question ??


def cart_detail(request: HttpRequest):
    cart = Cart(request)
    print(request.session[settings.CART_SESSION_ID])
    return render(request, 'cart/cart.html', {'cart': cart})




        
