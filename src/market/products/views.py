from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from .forms import ProductFeedbackForm
from market.categories.mixins import MenuMixin
from market.banner_app.mixins import BannerSliderMixin
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from market.products.models import Product, ProductFeedback
import logging

log = logging.getLogger(__name__)


class ProductDetailView(MenuMixin, BannerSliderMixin, LoginRequiredMixin, DetailView):
    template_name = 'products/product_details.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    form_class = ProductFeedbackForm

    def form_valid(self, form):
        response = super().form_valid(form)

        ProductFeedback.object.create(
            user=self.request.user,
            product=self.object,
            feedback_text=form,
        )
        # for image in form.files.getlist("images"):
        #     ProductImage.objects.create(
        #         product=self.object,
        #         image=image,
        #     )
        return response

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product_feedbacks'] = ProductFeedback.objects.filter(product=self.object)
        log.debug("Запуск рендеренга ProductDetailView")
        log.debug("Контекст для ProductDetailView готов. ")
        return context
