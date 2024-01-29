from .mixins import BannerSliderMixin, TopProductsMixin
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

from ..search_app.mixins import SearchMixin

log = logging.getLogger(__name__)

class IndexTemplateView(LoginRequiredMixin, TemplateView, BannerSliderMixin, MenuMixin, TopProductsMixin, SearchMixin):
    template_name = "banner_app/index.html"

