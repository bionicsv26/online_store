import logging
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from market.banner_app.mixins import BannerSliderMixin
from market.products.models import Product, ProductFeedback
from market.products.forms import ProductFeedbackForm
from market.categories.mixins import MenuMixin
from market.sellers.models import SellerProduct
from market.cart.cart import Cart

log = logging.getLogger(__name__)
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from market.categories.mixins import MenuMixin
from market.products.models import Product
from market.cart.cart import Cart


class ProductDetailView(MenuMixin, BannerSliderMixin, LoginRequiredMixin, DetailView):
    template_name = 'products/product_details.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    form_class = ProductFeedbackForm
    success_url = reverse_lazy('products:product-details')

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

    def post(self, request, *args, **kwargs):
        success_url = self.success_url
        form = self.form_class(request.POST)
        if form.is_valid():
            feedback_text = form.cleaned_data.get("feedback_text")
            ProductFeedback.objects.create(
                user=self.request.user,
                product=self.get_object(),
                feedback_text=feedback_text,
            )
            log.debug(f"Создан новый объект БД - отзыв на продукт. {self.get_object()} - {feedback_text}")
            return redirect(reverse(
                'products:product-details',
                kwargs={self.slug_url_kwarg: self.get_object().slug}
            ))
        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['product_feedbacks'] = (ProductFeedback.objects.
                                        prefetch_related('user', 'product').
                                        filter(product=self.object)
                                        )
        log.debug("Запуск рендеренга ProductDetailView")
        log.debug("Контекст для ProductDetailView готов. ")
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return Product.objects.prefetch_related('seller_products')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        amount = request.GET.get('amount')
        cart = Cart(request)
        
        return super().get(request, *args, **kwargs)
