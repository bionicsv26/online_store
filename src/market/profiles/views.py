from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import UserRegistrationForm
from ..sellers.models import SellerProduct
from market.banner_app.mixins import BannerSliderMixin
from market.categories.mixins import MenuMixin
from django.views.generic import (
    TemplateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from market.browsing_history_app.models import ProductBrowsingHistory
from market.products.models import Product
import logging

log = logging.getLogger(__name__)

class RegisterView(View):
    form_class = UserRegistrationForm
    initial = {'key': 'value'}
    template_name = 'profiles/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return redirect('market.profiles:login')

        return render(request, self.template_name, {'form': form})

class AccountTemplateView(LoginRequiredMixin, TemplateView, BannerSliderMixin, MenuMixin):
    template_name = "profiles/account.html"

    def get(self, request, *args, **kwargs):
        product_to_delete_from_browsing_history = self.request.GET.get('product_to_delete_from_browsing_history', 'none')
        if product_to_delete_from_browsing_history != 'none':
            product = Product.objects.get(slug=product_to_delete_from_browsing_history)
            log.debug(f"Получен сигнал об удалении продукта {product}")
            ProductBrowsingHistory.objects.filter(user=self.request.user, product=product).delete()
            log.debug(f"Продукт {product} удален из списка просмотренных товаров пользователя {self.request.user}")

        browsing_view = self.request.GET.get('browsing_view', 'short_list')
        if browsing_view == 'short_list':
            queryset = (ProductBrowsingHistory.
                        objects.
                        prefetch_related('user', 'product').
                        filter(user=self.request.user)[:3]
                        )
        elif browsing_view == 'long_list':
            queryset = (ProductBrowsingHistory.
                        objects.
                        prefetch_related('user', 'product').
                        filter(user=self.request.user)[:19]
                        )
        total_browsing_product_in_the_list = (ProductBrowsingHistory.
                                              objects.
                                              prefetch_related('user', 'product').
                                              filter(user=self.request.user)[:19]
                                              )
        context = self.get_context_data()
        context.update({
            'brosing_history': queryset,
            'total_browsing_product_in_the_list': total_browsing_product_in_the_list,
        })
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_user_name'] = self.request.user
        log.debug("Запуск рендеренга AccountTemplateView")
        log.debug("Контекст готов и передан на страницу account.html")
        return context


class ProfileTemplateView(LoginRequiredMixin, TemplateView, BannerSliderMixin, MenuMixin):
    template_name = "profiles/profile.html"


class CartDetailsView(TemplateView):
    template_name = 'profiles/cart_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.user.cart

        context['cart'] = cart
        context['seller_products'] = cart.seller_products.select_related(
            'discount',
            'discount__type',
            'product',
        ).prefetch_related(
            'product__categories',
        )
        context['discounted_cart_cost'], context['priority_discount_type'] = cart.get_priority_discounted_cost()

        return context
