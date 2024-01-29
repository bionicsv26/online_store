from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, reverse
from django.views.generic.base import ContextMixin, View

from market.search_app.forms import SearchForm


class SearchMixin(ContextMixin):
    search_form = SearchForm
    request = None

    def get_search_redirect_url(self, request: HttpRequest) -> str:
        search_form = self.search_form(request.POST)
        query = request.POST.get('query')
        if query and search_form.is_valid():
            match query:
                case str(query) if query.startswith('#'):
                    get_param = f'?tag={query[1:]}'
                case _:
                    get_param = f'?query={query}'

            return reverse('market.catalog_app:catalog') + get_param

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form(self.request.GET)
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        url = self.get_search_redirect_url(request)
        if url:
            return redirect(url)
