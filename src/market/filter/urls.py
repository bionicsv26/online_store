from django.urls import path

from .views import CatalogView

app_name = 'filter'

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    ]