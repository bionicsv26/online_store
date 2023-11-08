from market.categories.mixins import MenuMixin
from django.views.generic import (
    TemplateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)

from market.settingsapp.models import CacheTime
import logging

log = logging.getLogger(__name__)

class CatalogTemplateView(LoginRequiredMixin, TemplateView, MenuMixin):
    template_name = "catalog_app/catalog.html"

