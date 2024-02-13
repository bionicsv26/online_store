from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from market.categories.mixins import MenuMixin
from market.orders.models import OrderStatus
from market.products.models import Product
from market.search_app.mixins import SearchMixin
from market.sellers.models import Seller
from market.settingsapp.models import CacheTime


class SellerDetailsView(MenuMixin, View, SearchMixin):
    template_name = 'sellers/seller_details.html'

    def get(self, request: HttpRequest, seller_slug: str) -> HttpResponse:
        context = self.get_context_data(slug=seller_slug)
        return render(request, self.template_name, context=context)

    def get_context_data(self, **kwargs):
        """
        Метод получения контекстных данных, в котором кэшируются
        продавцы на день и топ продуктов продавца на час.
        """
        context = super().get_context_data(**kwargs)
        seller_slug = kwargs.get('slug')
        cache_settings = CacheTime.objects.all().first()

        seller = cache.get(f'seller_cache_{seller_slug}')
        if not seller:
            seller = get_object_or_404(Seller, slug=seller_slug)
            seller_cache_time = cache_settings.seller_data_cache
            cache.set(f'seller_cache_{seller_slug}', seller, seller_cache_time)

        products = cache.get(f'products_cache_{seller_slug}')
        if not products:
            payed_status = OrderStatus.objects.get(value='paid')
            products = Product.objects.filter(seller_products__seller=seller).prefetch_related(
                'categories__parent',
            ).annotate(
                paid_status_count=Count('seller_products__orders__status', filter=Q(seller_products__orders__status=payed_status))
            ).order_by('-paid_status_count')[:10]

            top_products_cache_time = cache_settings.top_products_cache
            cache.set(f'products_cache_{seller_slug}', products, top_products_cache_time)

        context['seller'] = seller
        context['products'] = products
        return context
