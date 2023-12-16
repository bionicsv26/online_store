from django.views.generic import DetailView
from .forms import ProductFeedbackForm
from market.categories.mixins import MenuMixin
from market.banner_app.mixins import BannerSliderMixin
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from market.products.models import Product, ProductFeedback
import logging
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect

log = logging.getLogger(__name__)


class ProductDetailView(MenuMixin, BannerSliderMixin, LoginRequiredMixin, DetailView):
    template_name = 'products/product_details.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    form_class = ProductFeedbackForm
    success_url = reverse_lazy('products:product-details')

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
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['product_feedbacks'] = ProductFeedback.objects.filter(product=self.object)
        log.debug("Запуск рендеренга ProductDetailView")
        log.debug("Контекст для ProductDetailView готов. ")
        return context
