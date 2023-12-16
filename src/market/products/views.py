from django.http import HttpResponseRedirect
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
from django.urls import reverse_lazy

log = logging.getLogger(__name__)


class ProductDetailView(MenuMixin, BannerSliderMixin, LoginRequiredMixin, DetailView):
    template_name = 'products/product_details.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    initial = {'feedback_text': 'Ваш королевский отзыв'}
    form_class = ProductFeedbackForm
    success_url = reverse_lazy('products:product-details')

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    # Handle POST GTTP requests
    def post(self, request, *args, **kwargs):
        success_url = self.success_url
        form = self.form_class(request.POST)
        if form.is_valid():
            feedback_text2 = form.cleaned_data.get("feedback_text")
            print("User put information to field 2 - feedback_text", feedback_text2)
            ProductFeedback.objects.create(
                user=self.request.user,
                product=self.get_object(),
                feedback_text=feedback_text2,
            )
            return HttpResponseRedirect(success_url)
        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        prod = self.object
        print("prod", prod)
        context['product_feedbacks'] = ProductFeedback.objects.filter(product=self.object)
        log.debug("Запуск рендеренга ProductDetailView")
        log.debug("Контекст для ProductDetailView готов. ")
        return context
