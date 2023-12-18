from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from ..products.models import Product


class CompareList:
    def __init__(self, request):
        self.request = request

        if 'compare_list' not in self.request.session:
            self.request.session['compare_list'] = []

    def parse_url_request_page(self):
        referer_url: str = self.request.META.get('HTTP_REFERER')
        string_reverse: str = ''
        dict_for_kwargs: dict = dict()
        if 'products/' in referer_url:
            list_referer_url = referer_url.split('products/')
            string_reverse = 'products:product-details'
            dict_for_kwargs = {"product_slug": list_referer_url[1]}
        elif 'categories/' in referer_url:
            list_referer_url = referer_url.split('categories/')
            match list_referer_url[1].count('/'):
                case 1:
                    string_reverse = 'categories:category-products-list'
                    dict_for_kwargs = {"category_slug": list_referer_url[1].strip('/')}
                case 2:
                    string_reverse = 'categories:subcategory-products-list'
                    split_kwargs = list_referer_url[1].strip('/').split('/')
                    dict_for_kwargs = {"category_slug": split_kwargs[0], "subcategory_slug": split_kwargs[1]}
        url_reverse = reverse(string_reverse, kwargs=dict_for_kwargs)
        return url_reverse

    def add_to_compare(self, product_id):
        if product_id not in self.request.session['compare_list']:
            self.request.session['compare_list'].append(product_id)
        self.request.session.modified = True

    def remove_from_compare(self, product_id):
        if product_id in self.request.session['compare_list']:
            self.request.session['compare_list'].remove(product_id)
            self.request.session.modified = True

    def get_compared_products(self):
        if 'compare_list' in self.request.session:
            return Product.objects.filter(pk__in=self.request.session['compare_list'])
        else:
            return []


class AddToCompareView(View):
    def get(self, request, product_id):
        compare_list = CompareList(request)
        compare_list.add_to_compare(product_id)
        url_reverse = compare_list.parse_url_request_page()
        return HttpResponseRedirect(url_reverse)


class RemoveFromCompareView(View):
    def get(self, request, product_id):
        compare_list = CompareList(request)
        compare_list.remove_from_compare(product_id)
        url_reverse = compare_list.parse_url_request_page()
        return HttpResponseRedirect(url_reverse)


class CompareListView(View):
    def get(self, request):
        compare_list = CompareList(request)
        compared_products = compare_list.get_compared_products()
        return render(request, 'comparison/comparison.html', {'compared_products': compared_products})
