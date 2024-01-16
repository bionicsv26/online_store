from .mixins import BannerSliderMixin, TopSellerProductsMixin
from market.categories.mixins import MenuMixin
from django.views.generic import (
    TemplateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from .models import BannerSlider
from market.settingsapp.models import CacheTime
import logging

log = logging.getLogger(__name__)

class IndexTemplateView(LoginRequiredMixin, TemplateView, BannerSliderMixin, MenuMixin, TopSellerProductsMixin):
    template_name = "banner_app/index.html"

