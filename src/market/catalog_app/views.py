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
from market.browsing_history_app.models import ProductBrowsingHistory

log = logging.getLogger(__name__)

def list_of_product_names(queryset):
    result_list = list()
    for i_product in queryset:
        result_list.append(i_product.product.name)
    return result_list

class CatalogTemplateView(LoginRequiredMixin, MenuMixin, ListView):
    template_name = "catalog_app/catalog.html"
    model = SellerProduct
    paginate_by = 8

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'price')
        if order_by == 'price' or order_by == '-created_at':
            return SellerProduct.objects.order_by(order_by)
        elif order_by == "feedback":
            queryset = SellerProduct.objects.annotate(
                num_feedbacks=Count('product__productfeedback__feedback_text')).order_by("-num_feedbacks")
            return queryset
        elif order_by == "rating":
            queryset = SellerProduct.objects.annotate(
                num_of_sale=Count('orders', filter=Q(orders__status__name='payed'))
            ).order_by("-num_of_sale")
            return queryset

    def get_context_data(self, **kwargs):
        context = super(CatalogTemplateView, self).get_context_data(**kwargs)
        order_by = self.request.GET.get('order_by', 'price')
        context['order_by'] = order_by
        browsing_history = ProductBrowsingHistory.objects.filter(user=self.request.user).all()
        context['browsing_history'] = list_of_product_names(browsing_history)
        log.debug("Запуск рендеренга CatalogOldTemplateView")
        log.debug("Контекст готов. Продукты отсортированы")
        return context
