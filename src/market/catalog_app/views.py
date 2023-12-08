from market.categories.mixins import MenuMixin
from django.views.generic import (
    ListView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from market.sellers.models import SellerProduct
from django.db.models import Q
import logging
from django.db.models import Count

log = logging.getLogger(__name__)


class CatalogTemplateView(LoginRequiredMixin, MenuMixin, ListView):
    template_name = "catalog_app/catalog.html"
    model = SellerProduct
    paginate_by = 8

    def get_queryset(self):
        if "order_by" in self.request.GET:
            order_by = self.request.GET.get('order_by', 'price')
            return SellerProduct.objects.order_by(order_by)
        elif "feedback" in self.request.GET:
            queryset = SellerProduct.objects.annotate(
                num_feedbacks=Count('product__feedback__feedback_text')).order_by("-num_feedbacks")
            return queryset
        elif "rating" in self.request.GET:
            queryset = SellerProduct.objects.annotate(
                num_of_sale=Count('orders', filter=Q(orders__status__name='payed'))
            ).order_by("-num_of_sale")
            return queryset
        else:
            log.debug("Ordered_by NOT in self.request.GET")
            return SellerProduct.objects.order_by('-price')

    def get_context_data(self, **kwargs):
        context = super(CatalogTemplateView, self).get_context_data(**kwargs)
        log.debug("Запуск рендеренга CatalogOldTemplateView")
        log.debug("Контекст готов. Продукты отсортированы")
        return context
