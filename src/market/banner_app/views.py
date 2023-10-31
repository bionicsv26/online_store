import random
from django.core.cache import cache
from django.views.generic import (
    TemplateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from .models import BannerSlider, ProjectSettings


class IndexTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "banner_app/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)

        # TODO изменить параметр "my_timeout" на информацию из приложения settingsapp - задача [MARKET-5]
        my_timeout = ProjectSettings.objects \
            .get(name="banners_sliders_cache_timeout") \
            .banners_sliders_cache_timeout
        context['banners_sliders_cache_timeout'] = my_timeout

        banners_sliders = cache.get("banners_sliders_cache")
        if not banners_sliders:
            queryset = BannerSlider.objects.filter(is_active=True)
            banners_sliders = random.sample(list(queryset), 3)
            cache.set("banners_sliders_cache", banners_sliders, my_timeout)
        context['banners_sliders'] = banners_sliders

        return context
