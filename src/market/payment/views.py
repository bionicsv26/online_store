import requests

from django.db.models import F
from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings


from .forms import PayForm
from ..orders.models import Order, OrderStatus
from ..categories.mixins import MenuMixin
from ..search_app.forms import SearchForm
from ..search_app.mixins import SearchMixin
from ..sellers.models import SellerProduct


class PayView(SearchMixin, MenuMixin, View):
    template_name = 'payment/payment.html'

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        order = Order.objects.get(pk=pk)
        if request.user.pk != order.user.pk:
            return HttpResponseForbidden()
        return render(request, self.template_name, context={
            'form': PayForm(),
            'search_form': SearchForm()
        })

    def post(self, request: HttpRequest, pk: int, *args, **kwargs) -> HttpResponse:
        response = super().post(request, *args, **kwargs)
        if response:
            return response

        form = PayForm(request.POST)
        if form.is_valid():
            order = Order.objects.get(pk=pk)
            data = {
                'pk': pk,
                'card_number': form.cleaned_data['card_number'],
            }
            url = settings.BANK_PAY_URL
            r = requests.post(url, data=data)
            if r.json()['paid']:
                order.status = OrderStatus.objects.get(value='paid')
                order.save()

                seller_products = SellerProduct.objects.filter(order_products__orders=order)
                seller_products.update(stock=F('stock') - 1)

            return redirect(reverse('orders:order_details', kwargs={'pk': order.pk}))

        context = self.get_context_data()
        context['form'] = form
        context['search_form'] = SearchForm()

        return render(request, self.template_name, context=context)
