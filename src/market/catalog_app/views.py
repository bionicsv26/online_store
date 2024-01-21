import logging

from django.db.models import Q, Min, Max
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
        queryset = self.model.objects.prefetch_related('seller_products').filter(seller_products__isnull=False)
        order_by = self.request.GET.get('order_by', 'price')
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.prefetch_related('seller_products').filter(
                Q(categories__slug=category) | Q(categories__parent__slug=category),
            )

        match order_by:
            case 'rating' | '-rating':
                queryset = queryset.annotate(
                    num_of_sale=Count('seller_products__orders', filter=Q(seller_products__orders__status__name='paid'))
                ).order_by('num_of_sale')

            case 'price' | '-price':
                queryset = queryset.annotate(
                    Min('seller_products__price')
                ).order_by('seller_products__price__min')

            case 'feedback' | '-feedback':
                queryset = queryset.annotate(
                    num_feedbacks=Count('productfeedback__feedback_text')
                ).order_by('num_feedbacks')

            case 'created_at' | '-created_at':
                queryset = queryset.annotate(
                    Max('seller_products__created_at')
                ).order_by('seller_products__created_at__max')

        return queryset.reverse() if order_by.startswith('-') else queryset

    def get_context_data(self, **kwargs):
        context = super(CatalogTemplateView, self).get_context_data(**kwargs)
        order_by = self.request.GET.get('order_by', 'price')
        category = self.request.GET.get('category')
        context['order_by'] = order_by
        context['category'] = category
        browsing_history = (ProductBrowsingHistory.objects.
                            select_related('user', 'product').
                            filter(user=self.request.user).
                            values_list("product__name", flat=True)
                            )
        context['browsing_history'] = browsing_history
        log.debug("Запуск рендеренга CatalogOldTemplateView")
        log.debug("Контекст готов. Продукты отсортированы")
        return context
