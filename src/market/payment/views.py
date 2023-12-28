from django.db.models import F
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings

import requests

from .forms import PayForm
from ..orders.models import Order, OrderStatus
from ..categories.mixins import MenuMixin


class PayView(MenuMixin, View):
    template_name = 'payment/payment.html'

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        order = Order.objects.get(pk=pk)
        if request.user.pk != order.user.pk:
            return HttpResponseForbidden()
        return render(request, self.template_name, context={'form': PayForm()})

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
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
                order.status = OrderStatus.objects.get(name='paid')
                order.save()

                order.seller_products.update(stock=F('stock') - 1)

                return redirect('payment:successfully', pk)

            return redirect('payment:unsuccessfully', pk)

        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context=context)


class PaymentSuccessfullyView(TemplateView):
    template_name = 'payment/successfully_payment.html'


class PaymentUnsuccessfullyView(TemplateView):
    template_name = 'payment/unsuccessfully_payment.html'
