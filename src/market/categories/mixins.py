from django.views.generic.base import ContextMixin

from market.categories.models import Category


class MenuMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent=None)
        return context
