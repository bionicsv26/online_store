from django.contrib import admin
from django.urls import path

from .views import IndexHtmlView, CategoryDetailsView, SubcategoryDetailsView

app_name = 'categories'

urlpatterns = [
    path('', IndexHtmlView.as_view(), name='index'),
    path('<slug:category_slug>/', CategoryDetailsView.as_view(), name='category-products-list'),
    path('<slug:category_slug>/<slug:subcategory_slug>/', SubcategoryDetailsView.as_view(), name='subcategory-products-list'),
]
