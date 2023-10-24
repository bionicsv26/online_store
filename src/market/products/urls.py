from django.contrib import admin
from django.urls import path

from market.products.views import ProductDetailView

app_name = 'products'

urlpatterns = [
    path('<slug:product_slug>', ProductDetailView.as_view(), name='product-details'),
]
