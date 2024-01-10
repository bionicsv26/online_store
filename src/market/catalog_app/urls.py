from django.urls import path
from .views import (
    CatalogTemplateView,
    FilterCatalogView,
)

app_name = 'market.catalog_app'

urlpatterns = [
    path('', CatalogTemplateView.as_view(), name='catalog'),
    path('filter/', FilterCatalogView.as_view(), name='filter'),
]
