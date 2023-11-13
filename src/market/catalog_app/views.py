from market.categories.mixins import MenuMixin
from django.views.generic import (
    ListView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from market.products.models import Product, ProductFeedback
from .models import SellerProduct

from market.settingsapp.models import CacheTime
import logging
from django.db.models import Count

log = logging.getLogger(__name__)



class CatalogTemplateView(LoginRequiredMixin, MenuMixin, ListView):
    template_name = "catalog_app/catalog.html"
    model = SellerProduct
    paginate_by = 8

    def get_queryset(self):
        print("self.request.GET", self.request.GET)
        if "order_by" in self.request.GET:
            print(" ordered_by in self.request.GET")
            order_by = self.request.GET.get('order_by', 'price')
            return SellerProduct.objects.order_by(order_by)
        elif "feedback" in self.request.GET:
            #qwery = SellerProduct.objects.annotate(num_feedbacks=Count('product__productfeedback__feedback_text')).order_by("num_feedbacks")
            qwery = SellerProduct.objects.annotate(num_feedbacks=Count('discount')).order_by("-num_feedbacks")
            print("qwery", qwery)
            return qwery
        else:
            print(" Ordered_by NOT in self.request.GET")
            return SellerProduct.objects.order_by('price')

    def get_context_data(self, **kwargs):
        context = super(CatalogTemplateView, self).get_context_data(**kwargs)
        log.debug("Запуск рендеренга CatalogOldTemplateView")

        feedbacks_count = ProductFeedback.objects.annotate(num_feedbacks=Count('feedback_text'))
        print("feedbacks_count", feedbacks_count)
        for item in context.items():
            print("Item ", item)
        log.debug("Контекст готов. Продукты отсортированы")
        return context
