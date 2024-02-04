from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from .models import Profile
from market.products.models import Product
from market.browsing_history_app.models import ProductBrowsingHistory
from .forms import UserProfileForm

from .forms import UserRegistrationForm
from ..orders.models import Order
from ..search_app.mixins import SearchMixin
from market.banner_app.mixins import BannerSliderMixin
from market.categories.mixins import MenuMixin
from django.contrib.auth.mixins import LoginRequiredMixin
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


class AccountTemplateView(LoginRequiredMixin, TemplateView, BannerSliderMixin, MenuMixin, SearchMixin):
    template_name = "profiles/account.html"

    def get(self, request, *args, **kwargs):
        product_to_delete_from_browsing_history = self.request.GET.get('product_to_delete_from_browsing_history',
                                                                       'none')
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
        context['last_order'] = Order.objects.filter(user=self.request.user).last()
        log.debug("Запуск рендеренга AccountTemplateView")
        log.debug("Контекст готов и передан на страницу account.html")
        return context


def clean_full_name(full_name:str) -> str | bool:
    split_data = full_name.split()
    if not ''.join(split_data).isalpha():
        return 'Это поле может содержать только буквы и пробелы'
    if len(split_data) != 3:
        return 'Это поле должно состоять из 3-х слов'
    for i_name in split_data:
        if not i_name[0].isupper():
            return 'Фамилия, Имя и Отчество должно быть с заглавной буквы'
    return True


class ProfileTemplateView(LoginRequiredMixin, TemplateView, BannerSliderMixin, MenuMixin, SearchMixin):
    template_name = "profiles/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial_data = {}
        if self.request.user.is_authenticated:
            log.debug("Пользователь авторизован, предзаполняем форму")
            user = self.request.user
            initial_data['email'] = user.email
            profile = user.profile
            initial_data['full_name'] = profile.full_name
            initial_data['phone'] = profile.phone
            initial_data['avatar'] = profile.avatar
        else:
            log.debug("Пользователь не авторизован, форма передается без предзаполнения")
        context['form'] = UserProfileForm(initial=initial_data)
        return context

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response:
            return response

        context = self.get_context_data()

        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            log.debug("Форма заполнена правильно. Проверка валидности прошла")
            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user=request.user.id)
            if 'avatar' in form.changed_data:
                print("if 'avatar' in form.changed_data:", form.cleaned_data['avatar'], type(form.cleaned_data['avatar']))
                profile.avatar = form.cleaned_data['avatar']
            if 'full_name' in form.changed_data:
                profile.full_name = form.cleaned_data['full_name']
            if 'phone' in form.changed_data:
                profile.phone = form.cleaned_data['phone']
            if 'email' in form.changed_data:
                user.email = form.cleaned_data['email']
            if ("password" in form.changed_data) and ("password_repeat" in form.changed_data):
                if form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                    log.debug("Введенные пароли отличаются. вызываем form.add_error")
                    form.add_error('password_repeat',
                                   'Пароль и подтверждение пароля не совпадают')
                    context.update({'form': form,
                                    "notification_password_error": "Профиль не сохранен. Пароли не совпадают"})

                    return render(request,
                                  self.template_name,context)
                else:
                    if form.cleaned_data['password'] != user.password:
                        user.set_password(form.cleaned_data['password'])
                        log.debug("Пароль был изменен.")
                        user.save()
                        profile.save()

                        user = authenticate(request,
                                            username=request.user.username,
                                            password=form.cleaned_data['password'])
                        if user is not None:
                            login(request, user)
                        context.update({'form': form,
                                        "notification_ok": "Профиль успешно сохранен."})

                        return render(request,
                                      self.template_name, context)
            user.save()
            profile.save()
            log.debug(f"Полученные из формы данные сохранены в БД User & Profile")
            context.update({'form': form,
                            "notification_ok": "Профиль успешно сохранен."})
            return render(request,
                          self.template_name, context)
        else:
            log.debug("Форма заполнена не правильно. Проверка валидности не пройдена. "
                      "Форма с описанием ошибки возвращается пользователю")
            context.update({'form': form,
                            "notification_form_validation_error": "Профиль не сохранен. "
                                                                 "Убедитесь, что все поля заполнены правильно "
                                                                 "и фотография выбрана."})
            return render(request,
                          self.template_name,context)

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


class OrdersHistoryView(LoginRequiredMixin, ListView, MenuMixin, SearchMixin):
    template_name = 'profiles/orders_history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
