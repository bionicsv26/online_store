from django.urls import path
from .views import (
    CatalogTemplateView
)

app_name = 'market.catalog_app'

urlpatterns = [
    path('', CatalogTemplateView.as_view(), name='catalog'),
]
