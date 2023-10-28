from django.urls import path

from .views import pay_handler_view


app_name = 'paymentsystem'

urlpatterns = [
    path('pay/', pay_handler_view, name='bank-pay'),
]
