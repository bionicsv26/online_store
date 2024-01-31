from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.http import HttpRequest, HttpResponse
from .cart import Cart
from market.products.models import Product
from ..categories.mixins import MenuMixin
from ..search_app.mixins import SearchMixin


class CartDetailsView(TemplateView, MenuMixin, SearchMixin):
    template_name = 'cart/cart.html'

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response = super().post(request, *args, **kwargs)
        if response:
            return response

        cart = Cart(request.session)
        if len(cart) > 0:
            for item in cart:
                seller_product = item.get('product')
                seller_product_pk = str(seller_product.pk)
                if seller_product_pk in request.POST:
                    quantity = request.POST.get(seller_product_pk)
                    if quantity.isdigit():
                        cart.add(seller_product, amount=int(quantity))

            return redirect(reverse('orders:making_an_order_page_1'))

        return self.render_to_response(self.get_context_data())


class CartAddView(View):
    
    def get(self, request: HttpRequest, product_id: str) -> HttpResponse:
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
