from django.contrib import messages
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView

from ..categories.mixins import MenuMixin
from ..products.models import Product
from ..search_app.mixins import SearchMixin
from ..sellers.models import SellerProduct


class CompareList:
    def __init__(self, session):
        self.session = session
        if 'compare_list' not in self.session:
            self.session['compare_list'] = []

    def add_to_compare(self, product_id: int) -> str:
        """Функция добавляет id выбранного товара в список для сравнения товаров"""
        if product_id not in self.session['compare_list'] and len(self.session['compare_list']) < 4:
            added_product = Product.objects.filter(id=product_id).first()
            if added_product is not None:
                self.session['compare_list'].append(product_id)
                message: str = f"Товар {added_product.name} добавлен в сравнение.\n"
                self.session.modified = True
                return message

    def remove_from_compare(self, product_id: int):
        """Функция удаляет id выбранного товара из списка для сравнения товаров"""
        if product_id in self.session['compare_list']:
            removed_product = Product.objects.filter(id=product_id).first()
            if removed_product is not None:
                self.session['compare_list'].remove(product_id)
                message: str = f"Товар {removed_product.name} удален из сравнения.\n"
                self.session.modified = True
                return message

    def get_compared_products(self):
        """Функция формирует queryset из товаров списка для сравнения"""
        if 'compare_list' in self.session and len(self.session['compare_list']) in range(2, 5):
            return (Product.objects.filter(id__in=self.session['compare_list'])
                    .prefetch_related("specification", "categories"))
        else:
            return []

    def get_prices_products(self):
        queryset = SellerProduct.objects.filter(
            product_id__in=self.session['compare_list'],
        ).values(
            "product_id",
        ).annotate(
            prices=ArrayAgg("price")
        ).order_by(
            "product_id",
        )
        return queryset


class AddToCompareView(MenuMixin, View):
    def get(self, request, product_id):
        compare_list = CompareList(self.request.session)
        message = compare_list.add_to_compare(product_id)
        if message is not None:
            messages.success(self.request, message)
        referer_url: str = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(referer_url)


class RemoveFromCompareView(MenuMixin, View):
    def get(self, request, product_id):
        compare_list = CompareList(self.request.session)
        message: str = compare_list.remove_from_compare(product_id)
        if message is not None:
            messages.success(self.request, message)
        referer_url: str = self.request.META.get('HTTP_REFERER')
        if len(self.request.session['compare_list']) == 1 and "comparison" in referer_url:
            product_id_last = self.request.session['compare_list'][0]
            compare_list.remove_from_compare(product_id_last)
        return HttpResponseRedirect(referer_url)


class CompareListView(SearchMixin, MenuMixin, TemplateView):
    template_name = 'comparison/comparison.html'

    def get_context_data(self, **kwargs):
        context = super(CompareListView, self).get_context_data(**kwargs)
        compare_list = CompareList(self.request.session)
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
            prices_compared_products = compare_list.get_prices_products()
            context['prices_products'] = prices_compared_products
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
