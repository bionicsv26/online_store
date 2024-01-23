from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetailsView.as_view(), name='cart_details'),
    path('add/<str:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('remove/<str:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
]
