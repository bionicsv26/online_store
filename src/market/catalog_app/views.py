from market.categories.mixins import MenuMixin
from django.views.generic import (
    ListView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
#TODO модель SellerProduct взять из реализации Задаче 9 от Андрея.
from .models import SellerProduct

import logging
from django.db.models import Count

log = logging.getLogger(__name__)


class CatalogTemplateView(LoginRequiredMixin, MenuMixin, ListView):
    template_name = "catalog_app/catalog.html"
    model = SellerProduct
    paginate_by = 8

    def get_queryset(self):
        if "order_by" in self.request.GET:
            # TODO проверить работоспособность после замены модели
            order_by = self.request.GET.get('order_by', 'price')
            return SellerProduct.objects.order_by(order_by)
        elif "feedback" in self.request.GET:
            #TODO проверить работоспособность после замены модели
            queryset = SellerProduct.objects.annotate(
                num_feedbacks=Count('product__product_feedbacks__feedback_text')).order_by("-num_feedbacks")
            return queryset
        elif "rating" in self.request.GET:
            #TODO Переделать на модель Андрея из задачи 9 -> SellerProduct сортировку по количеству покупок товара в соответствии с ТЗ
            queryset = SellerProduct.objects.annotate(
                num_of_view=Count('product__product_view_history__view_at')).order_by("-num_of_view")
            return queryset
        else:
            log.debug("Ordered_by NOT in self.request.GET")
            # TODO проверить работоспособность после замены модели
            return SellerProduct.objects.order_by('-price')

    def get_context_data(self, **kwargs):
        context = super(CatalogTemplateView, self).get_context_data(**kwargs)
        log.debug("Запуск рендеренга CatalogOldTemplateView")
        log.debug("Контекст готов. Продукты отсортированы")
        return context
