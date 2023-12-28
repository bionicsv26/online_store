from django.views.generic.base import ContextMixin

from market.categories.models import Category


class MenuMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_categories'] = [
            (category, category.categories.all())
            for category in Category.objects.prefetch_related('categories').filter(parent=None)
        ]
        return context
