import logging

from django.db.models import Q, Min, Max
from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from market.categories.mixins import MenuMixin
from market.products.models import Product
from django.db.models import Count
from market.browsing_history_app.models import ProductBrowsingHistory
from market.search_app.mixins import SearchMixin
from market.sellers.models import SellerProduct
from market.tags.models import Tag

log = logging.getLogger(__name__)


class CatalogTemplateView(SearchMixin, MenuMixin, ListView):
    template_name = "catalog_app/catalog.html"
    model = Product
    paginate_by = 8

    def get_queryset(self):
        queryset = self.model.objects.prefetch_related(
            'seller_products',
            'tags',
            'categories__parent',
        ).filter(seller_products__isnull=False)

        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(name__istartswith=query)

        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__name__istartswith=tag)

        category = self.request.GET.get('category')
        if category:
            queryset = queryset.prefetch_related('seller_products').filter(
                Q(categories__slug=category) | Q(categories__parent__slug=category),
            )

        order_by = self.request.GET.get('order_by', 'price')
        match order_by:
            case 'rating' | '-rating':
                queryset = queryset.annotate(
                    num_of_sale=Count('seller_products__orders', filter=Q(seller_products__orders__status__value='paid'))
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

        price_range = self.request.GET.get('price_filter')
        if price_range:
            price_range = price_range.split(";")
            range_start = price_range[0]
            range_end = price_range[1]
            queryset = queryset.filter(seller_products__price__range=(range_start, range_end))

        title = self.request.GET.get('title')
        in_stock = self.request.GET.get('in_stock')

        if title:
            queryset = queryset.filter(
                Q(name__icontains=title) | Q(description__icontains=title)
            )

        if in_stock:
            queryset = queryset.filter(seller_products__stock__gt=0)

        return queryset.reverse() if order_by.startswith('-') else queryset

    def get_context_data(self, **kwargs):
        context = super(CatalogTemplateView, self).get_context_data(**kwargs)
        order_by = self.request.GET.get('order_by', 'price')
        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')
        query = self.request.GET.get('query')

        context['order_by'] = order_by
        context['category'] = category
        context['tag'] = tag
        context['max_price'] = SellerProduct.objects.aggregate(Max('price'))['price__max']
        context['price_filter'] = self.request.GET.get('price_filter')

        if context['price_filter']:
            context['set_price'] = context['price_filter'].split(";")[1]

        context['title'] = self.request.GET.get('title')
        context['in_stock'] = self.request.GET.get('in_stock')

        if self.request.user.is_authenticated:
            browsing_history = (ProductBrowsingHistory.objects.
                                select_related('user', 'product').
                                filter(user=self.request.user).
                                values_list("product__name", flat=True)
                                )
            context['browsing_history'] = browsing_history

        context['popular_tags'] = Tag.objects.annotate(total_products=Count('products')).order_by('-total_products')[:5]
        context['query'] = query
        log.debug("Запуск рендеренга CatalogOldTemplateView")
        log.debug("Контекст готов. Продукты отсортированы")
        return context
