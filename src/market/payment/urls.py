from django.urls import path

from .views import PayView, PaymentSuccessfullyView, PaymentUnsuccessfullyView

app_name = 'payment'

urlpatterns = [
    path('payment/', PayView.as_view(), name='payment'),
    path('payment/successfully/', PaymentSuccessfullyView.as_view(), name='successfully'),
    path('payment/unsuccessfully/', PaymentUnsuccessfullyView.as_view(), name='unsuccessfully'),
]
