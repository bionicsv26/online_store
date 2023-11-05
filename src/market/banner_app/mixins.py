from django.views.generic.base import ContextMixin
import random
from django.core.cache import cache
from .models import BannerSlider
from market.settingsapp.models import CacheTime
import logging

log = logging.getLogger(__name__)

class BannerSliderMixin(ContextMixin):
    '''
    Миксин проверяет кэш "banners_sliders_cache" и если его нет, создает его.
    После проверки или создания возвращает сонтекст, который используется в рендере.
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        log.debug("Start BannerSliderMixin to prepare BannerSlider")
        my_timeout = CacheTime.objects.get(pk=1).banners_cache

        banners_sliders = cache.get("banners_sliders_cache")
        if not banners_sliders:
            queryset = BannerSlider.objects.filter(is_active=True)
            if queryset:
                banners_sliders = random.sample(list(queryset), 3)
                cache.set("banners_sliders_cache", banners_sliders, my_timeout)
                log.debug("Banners uploaded from DB and saved on cache: %s", banners_sliders)

        context['banners_sliders'] = banners_sliders

        return context
