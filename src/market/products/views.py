from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView
from .forms import ProductFeedbackForm
from market.categories.mixins import MenuMixin
from market.banner_app.mixins import BannerSliderMixin
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from market.products.models import Product, ProductFeedback
from market.browsing_history_app.models import ProductBrowsingHistory
import logging
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect

from ..search_app.mixins import SearchMixin

from market.cart.cart import Cart
from market.sellers.models import SellerProduct



log = logging.getLogger(__name__)


class ProductDetailView(MenuMixin, BannerSliderMixin, LoginRequiredMixin, DetailView, SearchMixin):
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
        cart = Cart(request.session)
        amount = request.GET.get('amount')
        seller_product_id = request.GET.get('seller_product_id')

        if seller_product_id is None:
            product = self.get_object()
            seller_product = product.seller_products.order_by('price').first()
        else:
            seller_product = SellerProduct.objects.get(id=seller_product_id)
            amount = 1

        if amount or seller_product_id:
            cart.add(seller_product, int(amount))

        return response

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response:
            return response

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

        # Проверяем, был ли данный товар уже в списке ранее просмотренных товаров. Если нет, то добавляем
        # Если товар уже в списке, то не добавляем
        products = (ProductBrowsingHistory.objects.
                    select_related('user', 'product').
                    filter(user=self.request.user))
        product = self.get_object()
        if not products.filter(product=product).exists():
            ProductBrowsingHistory.objects.create(
                user=self.request.user,
                product=product,
            )
        browsing_history = (ProductBrowsingHistory.objects.
                            select_related('user', 'product').
                            filter(user=self.request.user).
                            values_list("product__name", flat=True)
                            )
        context['browsing_history'] = browsing_history
        context['product_tags'] = context['product'].tags.all()
        log.debug("Запуск рендеренга ProductDetailView")
        log.debug("Контекст для ProductDetailView готов. ")
        return context
