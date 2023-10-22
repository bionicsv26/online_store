import random
from django.shortcuts import render
from django.http import (
    HttpRequest,
)
from django.views.generic import (
    TemplateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from .models import BannerSlider, Product, ProjectSettings


class IndexTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "banner_app/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)

        # Take all banners from DB and choose randomly only 3 of them
        queryset = BannerSlider.objects.filter(is_active=True)
        banners_sliders = random.sample(list(queryset), 3)

        # TODO change "my_timeout" delay for information from settings file due to [MARKET-5] task
        my_timeout = ProjectSettings.objects.get(name="banners_sliders_cache_timeout").banners_sliders_cache_timeout

        context['banners_sliders'] = banners_sliders
        context['banners_sliders_cache_timeout'] = my_timeout
        return context
