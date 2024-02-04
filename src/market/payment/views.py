import requests
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import F
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.views import View
from django.conf import settings


from .forms import PayForm
from ..orders.models import Order, OrderStatus
from ..categories.mixins import MenuMixin
from ..search_app.mixins import SearchMixin


class PayView(LoginRequiredMixin, View, MenuMixin, SearchMixin):
    template_name = 'payment/payment.html'

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        not_paid_status = OrderStatus.objects.get(value='not_paid')
        order = get_object_or_404(Order, pk=pk, status=not_paid_status)
        if request.user.pk != order.user.pk:
            return HttpResponseForbidden()

        context = self.get_context_data()
        context.update({'form': PayForm()})
        return render(request, self.template_name, context=context)

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

                order.seller_products.update(stock=F('stock') - 1)

            return redirect(reverse('orders:order_details', kwargs={'pk': order.pk}))

        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context=context)
