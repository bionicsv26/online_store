from market.categories.mixins import MenuMixin
from django.views.generic import (
    ListView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from market.products.models import Product

from market.settingsapp.models import CacheTime
import logging

log = logging.getLogger(__name__)



class CatalogTemplateView(LoginRequiredMixin, MenuMixin, ListView):
    template_name = "catalog_app/catalog.html"
    model = Product
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(CatalogTemplateView, self).get_context_data(**kwargs)
        log.debug("Запуск рендеренга CatalogOldTemplateView")

        for item in context.items():
            print("Item ", item)
        log.debug("Контекст готов. Продукты отсортированы")
        return context
