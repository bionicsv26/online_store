from django.urls import path

from .views import PayView

app_name = 'payment'

urlpatterns = [
    path('payment/', PayView.as_view(), name='payment'),
]
