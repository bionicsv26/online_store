from django.views.generic.base import ContextMixin

from market.categories.models import Category


class MenuMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.prefetch_related('categories').filter(parent=None)
        subcategories = [
            subcategory
            for category in categories
            for subcategory in category.categories.all()
        ]
        context['menu_categories'] = categories
        context['menu_subcategories'] = subcategories
        return context
