import random
from django.core.cache import cache
from django.views.generic import (
    TemplateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from .models import BannerSlider, ProjectSettings
import logging

log = logging.getLogger(__name__)

class IndexTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "banner_app/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        log.debug("Запуск IndexTemplateView для рендеренга index.html")
        # TODO изменить параметр "my_timeout" на информацию из приложения settingsapp - задача [MARKET-5]
        my_timeout = ProjectSettings.objects \
            .get(name="banners_sliders_cache_timeout") \
            .banners_sliders_cache_timeout
        context['banners_sliders_cache_timeout'] = my_timeout

        banners_sliders = cache.get("banners_sliders_cache")
        if not banners_sliders:
            queryset = BannerSlider.objects.filter(is_active=True)
            if queryset:
                banners_sliders = random.sample(list(queryset), 3)
                cache.set("banners_sliders_cache", banners_sliders, my_timeout)
                log.debug("Банеры выгружены из БД и загружены в кэш: %s", banners_sliders)
        context['banners_sliders'] = banners_sliders
        log.debug("Банеры загружены из кэша: %s", banners_sliders)

        return context
