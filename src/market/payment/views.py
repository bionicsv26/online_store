from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.conf import settings

import requests

from .forms import PayForm
from ..orders.models import Order, OrderStatus


class PayView(TemplateView):
    template_name = 'payment/payment.html'

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
            if r.json()['payed']:
                order.status = OrderStatus.objects.get(name='payed')
                order.save()
                return redirect('payment:successfully', pk)

            return redirect('payment:unsuccessfully', pk)

        return render(request, self.template_name, context={'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PayForm()
        context['form'] = form
        return context


class PaymentSuccessfullyView(TemplateView):
    template_name = 'payment/successfully_payment.html'


class PaymentUnsuccessfullyView(TemplateView):
    template_name = 'payment/unsuccessfully_payment.html'
