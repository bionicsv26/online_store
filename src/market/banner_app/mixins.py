from django.views.generic.base import ContextMixin
import random
from django.core.cache import cache
from .models import BannerSlider
from market.settingsapp.models import CacheTime
from django.db.models import Count, Q
import logging

from ..products.models import Product, ProductFeedback

log = logging.getLogger(__name__)


class BannerSliderMixin(ContextMixin):
    '''
    Миксин проверяет кэш "banners_sliders_cache" и если его нет, создает его.
    После проверки или создания возвращает контекст, который используется в рендере.
    '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        log.debug("Start BannerSliderMixin to prepare BannerSlider")
        my_timeout = CacheTime.objects.first().banners_cache

        banners_sliders = cache.get("banners_sliders_cache")
        if not banners_sliders:
            queryset = BannerSlider.objects.filter(is_active=True)
            if queryset:
                banners_sliders = random.sample(list(queryset), 3)
                cache.set("banners_sliders_cache", banners_sliders, my_timeout)
                log.debug("Banners uploaded from DB and saved on cache: %s", banners_sliders)

        context['banners_sliders'] = banners_sliders

        return context


class TopProductsMixin(ContextMixin):
    '''
    Миксин проверяет кэш "top_products_cache" и если его нет, создает его.
    Берет из БД товары продавцов, отсортированных по количеству продаж.
    После проверки или создания возвращает контекст, который используется в рендере.
    '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        log.debug("Start TopProductsMixin to prepare Top Seller products for Index page")
        top_products_timeout = CacheTime.objects.first().top_products_cache
        log.debug(f"top_products_timeout is: {top_products_timeout}")
        top_products = cache.get("top_products_cache")
        if not top_products:
            log.debug(f"There is no top_products in the cache yet")
            queryset = Product.objects.prefetch_related('categories__parent').annotate(
                num_of_sale=Count('seller_products__orders', filter=Q(seller_products__orders__status__value='paid'))
            ).order_by("-num_of_sale")

            if queryset.exists():
                log.debug(
                    f"Products upload from DB and ordered by number of sale {queryset}. "
                    f"There is : {len(queryset)} objects")
                cache.set("top_products_cache", queryset, top_products_timeout)
                log.debug(f"Products upload from DB and saved on cache: {queryset}")
                top_products = queryset
            else:
                log.debug(f"There is no any products upload from DB")
        else:
            log.debug(f"top_products was taken from the cache {top_products}."
                  f"\nNumber of products is {len(top_products)}")
        if len(top_products) >= 8:
            context['top_products_card'] = top_products[:4]
            context['top_products_card_hide_md'] = top_products[4:6]
            context['top_products_card_hide_md_hide_1450'] = top_products[6:8]
        elif 0 < len(top_products) < 8:
            context['top_products_card'] = top_products

        return context


class TopRatingProductsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_rating_products = Product.objects.annotate(
            num_of_feedbacks=Count('productfeedback')
        ).order_by("-num_of_feedbacks")[:5]
        log.debug(f"top_rating_products: {top_rating_products}, len = {len(top_rating_products)}")

        context['top_rating_product'] = random.choice(top_rating_products)

        return context