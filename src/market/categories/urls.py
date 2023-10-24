from django.contrib import admin
from django.urls import path

from .views import IndexHtmlView, CategoriesDetailsView, SubcategoriesDetailsView

app_name = 'categories'

urlpatterns = [
    path('', IndexHtmlView.as_view(), name='index'),
    path('<slug:category_slug>-subcategories/', CategoriesDetailsView.as_view(), name='category-details'),
    path('<slug:category_slug>-subcategories/<slug:subcategory_slug>/', SubcategoriesDetailsView.as_view(), name='subcategory-details'),
]
