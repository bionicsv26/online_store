from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from .models import Category
from .mixins import MenuMixin
from market.banner_app.mixins import BannerSliderMixin


class IndexHtmlView(MenuMixin, TemplateView, BannerSliderMixin):
    template_name = 'categories/index.html'


def get_products(category):
    if not category.parent:
        products = [
            product
            for category in category.categories.all()
            for product in category.products.all()
        ]
    else:
        products = category.products.all()

    return products


class CategoryDetailsView(MenuMixin, DetailView):
    template_name = 'categories/category_products_list.html'
    queryset = Category.objects.prefetch_related('products')
    context_object_name = 'category'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['category']
        context['products'] = get_products(category)
        return context


class SubcategoryDetailsView(CategoryDetailsView):
    slug_url_kwarg = 'subcategory_slug'
