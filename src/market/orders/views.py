from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.core.cache import cache
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy

from rest_framework.viewsets import ModelViewSet

from .forms import OrderCreationPage1Form, OrderCreationPage2Form, OrderCreationPage3Form
from .models import Order, OrderStatus, Cart
from .serializers import OrderSerializer
from ..categories.mixins import MenuMixin


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class MakingOrderTemplateViewMixin(MenuMixin, TemplateView):
    template_name = 'orders/making_an_order.html'


class CheckUserCacheMixin(UserPassesTestMixin):
    current_page = None

    def test_func(self):
        form_cache = cache.get(f'order_create_{self.request.user.id}')
        if not form_cache:
            form_cache = dict()

        if not form_cache or form_cache['current_page'] < self.page:
            self.current_page = form_cache.get('current_page', 1)
            return False

        return True

    def handle_no_permission(self):
        return redirect(f'orders:making_an_order_page_{self.current_page}')


class MakingOrderViewMixin(LoginRequiredMixin, MakingOrderTemplateViewMixin, FormView):
    success_url = reverse_lazy('orders:making_an_order')
    page = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form_cache = cache.get(f'order_create_{self.request.user.id}')
        if form_cache:
            form_data = form_cache.get(f'form_{self.page}')
            if form_data:
                form = self.form_class(form_data)
                context['form'] = form
        else:
            form_cache = dict()

            # предзаполнение данных пользователя
            user = self.request.user
            user_profile = self.request.user.profile
            form = self.form_class({
                'full_name': user_profile.full_name,
                'phone': user_profile.phone,
                'email': user.email,
            })
            context['form'] = form

        context['current_page'] = form_cache.get('current_page', 1)
        context['page'] = self.page
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form_cache = cache.get(f'order_create_{self.request.user.id}')
            if form_cache:
                form_cache[f'form_{self.page}'] = form.cleaned_data
                if self.page == form_cache.get('current_page'):
                    form_cache['current_page'] += 1
            else:
                form_cache = {
                    f'form_{self.page}': form.cleaned_data,
                    'current_page': self.page + 1,
                }

            cache.set(f'order_create_{self.request.user.id}', form_cache, 3600)

            return redirect(f'orders:making_an_order_page_{self.page + 1}')

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class MakingOrderPage1View(MakingOrderViewMixin):
    form_class = OrderCreationPage1Form
    success_url = reverse_lazy('orders:making_an_order_page_2')
    page = 1


class MakingOrderPage2View(CheckUserCacheMixin, MakingOrderViewMixin):
    form_class = OrderCreationPage2Form
    success_url = reverse_lazy('orders:making_an_order_page_3')
    page = 2


class MakingOrderPage3View(CheckUserCacheMixin, MakingOrderViewMixin):
    form_class = OrderCreationPage3Form
    success_url = reverse_lazy('orders:making_an_order_page_4')
    page = 3


class MakingOrderPage4View(CheckUserCacheMixin, MakingOrderTemplateViewMixin):
    page = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form_cache = cache.get(f'order_create_{self.request.user.id}')
        forms = {
            'form_1': OrderCreationPage1Form(form_cache['form_1']),
            'form_2': OrderCreationPage2Form(form_cache['form_2']),
            'form_3': OrderCreationPage3Form(form_cache['form_3']),
        }
        cart = Cart.objects.prefetch_related(
            'seller_products',
            'seller_products__product',
        ).get(user=self.request.user)
        seller_products = cart.seller_products.all()

        context.update({
            'page': self.page,
            'current_page': form_cache.get('current_page'),
            'forms': forms,
            'cart': cart,
            'seller_products': seller_products
        })
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        form_data = cache.get(f'order_create_{request.user.id}')
        if not form_data:
            return redirect('orders:making_an_order_page_1')

        form_1, form_2, form_3 = (value for key, value in form_data.items() if key.startswith('form_'))

        # создание заказа
        not_payed_order_status = OrderStatus.objects.get(name='not paid')
        order = Order.objects.create(
            user=request.user,
            full_name=form_1['full_name'],
            phone=form_1['phone'],
            email=form_1['email'],
            delivery_city=form_2['delivery_city'],
            delivery_address=form_2['delivery_address'],
            delivery_method=form_2['delivery_method'],
            payment_method=form_3['payment_method'],
            status=not_payed_order_status,
        )

        # добавление в заказ продуктов из корзины
        order.seller_products.set(request.user.cart.seller_products.all())

        cache.delete(f'order_create_{self.request.user.id}')
        return redirect(reverse('payment:payment', kwargs={'pk': order.pk}))
