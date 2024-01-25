from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import UserRegistrationForm
from django.urls import reverse_lazy, reverse
from .forms import UserRegistrationForm, UserProfileForm
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
from django.contrib.auth.models import User
from .models import Profile
from market.products.models import Product
import logging

log = logging.getLogger(__name__)

class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'profiles/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт для {username} создан.')

            return redirect(to=reverse('market.profiles:login'))

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
    #form_class = UserProfileForm

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST)
        if form.is_valid():
            print("The form is valid")
            full_name = form.cleaned_data.get("full_name")
            phone = form.cleaned_data.get("phone")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            password_repeat = form.cleaned_data.get("password_repeat")
            print("full_name is  ----    ", full_name)
            print("phone is  ----    ", phone)
            print("email is  ----    ", email)
            print("password is  ----    ", password)
            print("password_repeat is  ----    ", password_repeat)
            print("request.user  ----    ", request.user)
            user = User.objects.get(id=request.user.id)
            user.email = email
            user.save()
            profile = Profile.objects.get(user=request.user.id)
            profile.phone = phone
            profile.save()
            log.debug(f"Form was saved")
            return redirect(reverse(
                'market.profiles:profile'
            ))
        else:
            print("The form is not valid")
            return self.render_to_response({'form': form})
        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserProfileForm()

        log.debug("Запуск рендеренга ProfileTemplateView")
        log.debug("Контекст для form готов. ")
        return context


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
