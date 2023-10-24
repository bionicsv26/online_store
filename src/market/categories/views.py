from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from .models import Category
from .mixins import MenuMixin


class IndexHtmlView(MenuMixin, TemplateView):
    template_name = 'categories/index.html'


class CategoriesDetailsView(MenuMixin, DetailView):
    template_name = 'categories/category_details.html'
    model = Category
    context_object_name = 'category'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['category']
        context['subcategories'] = category.categories.all()
        return context


class SubcategoriesDetailsView(MenuMixin, DetailView):
    template_name = 'categories/subcategories.html'
    queryset = Category.objects.prefetch_related('products')
    context_object_name = 'subcategory'
    slug_url_kwarg = 'subcategory_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = context['subcategory'].products.filter(is_active=True)
        return context
