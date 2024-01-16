from typing import Optional

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from ..categories.mixins import MenuMixin
from ..products.models import Product
from ..sellers.models import SellerProduct


class CompareList:
    def __init__(self, request):
        self.request = request
        if 'compare_list' not in self.request.session:
            self.request.session['compare_list'] = []

    def parse_url_request_page(self):
        """
        Функция возвращает url исходной страницы с параметрами для возврата на нее же
        после выполнения методов add_to_compare и remove_from_compare
        """
        referer_url: str = self.request.META.get('HTTP_REFERER')
        string_reverse: str = ''
        dict_for_kwargs: Optional[dict] = dict()
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
        elif 'comparison/' in referer_url:
            string_reverse = 'comparison:compared_products'
            dict_for_kwargs = None
        url_reverse = reverse(string_reverse, kwargs=dict_for_kwargs)
        return url_reverse

    def add_to_compare(self, product_id):
        """Функция добавляет id выбранного товара в список для сравнения товаров"""
        if product_id not in self.request.session['compare_list'] and len(self.request.session['compare_list']) < 4:
            self.request.session['compare_list'].append(product_id)
            added_product = Product.objects.filter(id=product_id).first()
            message: str = f"Товар {added_product.name} добавлен в сравнение.\n"
            messages.success(self.request, message)
        self.request.session.modified = True

    def remove_from_compare(self, product_id):
        """Функция удаляет id выбранного товара из списка для сравнения товаров"""
        if product_id in self.request.session['compare_list']:
            self.request.session['compare_list'].remove(product_id)
            removed_product = Product.objects.filter(id=product_id).first()
            message: str = f"Товар {removed_product.name} удален из сравнения.\n"
            messages.success(self.request, message)
            self.request.session.modified = True

    def get_compared_products(self):
        """Функция формирует queryset из товаров списка для сравнения"""
        if 'compare_list' in self.request.session and len(self.request.session['compare_list']) in range(2, 5):
            return (Product.objects.filter(id__in=self.request.session['compare_list'])
                    .prefetch_related("specification"))
        else:
            return []

    def get_prices_products(self):
        """Функция формирует словарь цен для товаров из списка для сравнения"""
        dict_prices_products: dict = dict()
        queryset = (SellerProduct.objects.filter(product_id__in=self.request.session['compare_list'])
                    .only("product_id", "price"))
        for item_id in self.request.session['compare_list']:
            list_prices: list = list()
            for item in queryset.filter(product_id=item_id):
                list_prices.append(item.price)
            if len(list_prices) > 1:
                dict_prices_products.update({item_id: f"{min(list_prices)} - {max(list_prices)}"})
            else:
                dict_prices_products.update({item_id: f"{min(list_prices)}"})
        return dict_prices_products


class AddToCompareView(MenuMixin, View):
    def get(self, request, product_id):
        compare_list = CompareList(request)
        compare_list.add_to_compare(product_id)
        url_reverse = compare_list.parse_url_request_page()
        return HttpResponseRedirect(url_reverse)


class RemoveFromCompareView(MenuMixin, View):
    def get(self, request, product_id):
        compare_list = CompareList(request)
        compare_list.remove_from_compare(product_id)
        url_reverse = compare_list.parse_url_request_page()
        if len(self.request.session['compare_list']) == 1 and "comparison" in url_reverse:
            product_id_last = self.request.session['compare_list'][0]
            compare_list.remove_from_compare(product_id_last)
        return HttpResponseRedirect(url_reverse)


class CompareListView(MenuMixin, TemplateView):
    template_name = 'comparison/comparison.html'

    def get_context_data(self, **kwargs):
        context = super(CompareListView, self).get_context_data(**kwargs)
        compare_list = CompareList(self.request)
        compared_products = compare_list.get_compared_products()
        only_categories: list = list()
        for product in compared_products:
            for category in product.categories.all():
                only_categories.append(category)
        if len(set(only_categories)) != 1:
            messages.success(self.request, "Сравниваемые между собой товары должны быть из одной категории ")
        else:
            context['different_categories'] = True
        if len(compared_products) > 0:
            dict_prices_products = compare_list.get_prices_products()
            context['prices_products'] = dict_prices_products
        if self.request.GET.get('checkbox_only_diff') == 'on':
            list_differences = create_list_differences(compared_products)
            context['checked'] = True
        else:
            list_differences = None
            context['checked'] = False
            context['list_specifications'] = create_list_specifications(compared_products)
        context['compared_products'] = compared_products
        context['list_differences'] = list_differences
        return context


def create_list_differences(compared_products: CompareList) -> list:
    """
    Функция формирует список характеристик модели Specification,
    значения которых для выбранных товаров отличаются
    """
    dict_only_diff: dict = dict()
    list_differences: list = list()
    for item in compared_products:
        for spec in item.specification.all():
            if spec.name not in dict_only_diff:
                dict_only_diff[spec.name] = []
            dict_only_diff[spec.name].append(spec.value)
    for key, value in dict_only_diff.items():
        if len(set(value)) > 1:
            list_differences.append(key)
    return list_differences


def create_list_specifications(compared_products: CompareList) -> list:
    """Функция формирует полный список характеристик модели Specification для выбранных товаров"""
    list_specifications: list = list()
    for item in compared_products:
        for spec in item.specification.all():
            list_specifications.append(spec.name)
    if len(set(list_specifications)) == len(list_specifications):
        list_specifications.clear()
    else:
        list_specifications = list(set(list_specifications))
    return list_specifications

