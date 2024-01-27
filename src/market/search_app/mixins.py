from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, reverse
from django.views.generic.base import ContextMixin

from market.search_app.forms import SearchForm


class SearchMixin(ContextMixin):
    search_form = SearchForm

    def get_search_redirect_url(self, request: HttpRequest) -> str:
        search_form = self.search_form(request.POST)
        query = request.POST.get('query')
        if query and search_form.is_valid():
            return reverse('market.catalog_app:catalog') + f'?query={query}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form(context)
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        url = self.get_search_redirect_url(request)
        if url:
            return redirect(url)
