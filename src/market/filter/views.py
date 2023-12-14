from market.categories.mixins import MenuMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CatalogView(TemplateView, MenuMixin, LoginRequiredMixin):
    template_name = 'categories/category_products_list.html'


class FilterMixin:
    



