from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from market.categories.mixins import MenuMixin
from market.orders.models import OrderStatus
from market.sellers.models import Seller
from market.settingsapp.models import CacheTime


class SellerListView(ListView):
    template_name = 'sellers/sellers_list.html'
    model = Seller
    context_object_name = 'sellers'


class SellerDetailsView(MenuMixin, View):
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
        seller_products = cache.get(f'seller_products_cache_{seller_slug}')

        if not seller:
            seller = get_object_or_404(Seller, slug=seller_slug)
            seller_cache_time = cache_settings.seller_data_cache
            cache.set(f'seller_cache_{seller_slug}', seller, seller_cache_time)

        if not seller_products:
            payed_status = OrderStatus.objects.get(name='paid')

            seller_products = seller.seller_products.select_related(
                'product', 'discount'
            ).prefetch_related(
                'product__categories',
                'orders__status',
            ).annotate(
                paid_status_count=Count('orders__status', filter=Q(orders__status__name=payed_status.name))
            ).order_by('-paid_status_count')[:10]

            top_seller_products_cache_time = cache_settings.top_products_cache
            cache.set(f'seller_products_cache_{seller_slug}', seller_products, top_seller_products_cache_time)

        context['seller'] = seller
        context['seller_products_categories'] = [
            (seller_product, seller_product.product.categories.all())
            for seller_product in seller_products
        ]
        return context
