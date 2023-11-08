from market.categories.mixins import MenuMixin
from django.views.generic import (
    TemplateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from market.products.models import Product

from market.settingsapp.models import CacheTime
import logging

log = logging.getLogger(__name__)


class CatalogTemplateView(LoginRequiredMixin, TemplateView, MenuMixin):
    template_name = "catalog_app/catalog.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        log.debug("Запуск рендеренга ProductDetailView")
        products = Product.objects.all()
        print("products", products)
        for product in products:
            print("Object product", product, type(product))
            for category in product.category.all():
                print("Category ", type(category), category.name)
        context['products'] = products
        log.debug("Контекст готов. Продукты отсортированы", context)
        return context
