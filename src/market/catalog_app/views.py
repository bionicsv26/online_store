import logging

from django.db.models import Count, Q, Min
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from market.categories.mixins import MenuMixin
from market.products.models import Product
from django.db.models import Count
from market.browsing_history_app.models import ProductBrowsingHistory

log = logging.getLogger(__name__)


class CatalogTemplateView(LoginRequiredMixin, MenuMixin, ListView):
    template_name = "catalog_app/catalog.html"
    model = Product
    paginate_by = 8

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'price')
        queryset = self.model.objects.prefetch_related('seller_products')
        if order_by in ('price', '-price'):
            return queryset.annotate(Min('seller_products__price')).order_by(
                 '{}seller_products__price__min'.format('-' if order_by == '-price' else '')
            )

        elif order_by == '-created_at':
            return queryset.order_by(order_by)

        elif order_by == "feedback":
            return queryset.annotate(
                num_feedbacks=Count('productfeedback__feedback_text')
            ).order_by("-num_feedbacks")

        elif order_by == "rating":
            return queryset.annotate(
                num_of_sale=Count('seller_products__orders', filter=Q(seller_products__orders__status__name='payed'))
            ).order_by("-num_of_sale")

    def get_context_data(self, **kwargs):
        context = super(CatalogTemplateView, self).get_context_data(**kwargs)
        order_by = self.request.GET.get('order_by', 'price')
        context['order_by'] = order_by
        browsing_history = (ProductBrowsingHistory.objects.
                            select_related('user', 'product').
                            filter(user=self.request.user).
                            values_list("product__name", flat=True)
                            )
        context['browsing_history'] = browsing_history
        log.debug("Запуск рендеренга CatalogOldTemplateView")
        log.debug("Контекст готов. Продукты отсортированы")
        return context
