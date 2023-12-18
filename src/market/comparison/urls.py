from django.urls import path

from .views import AddToCompareView, RemoveFromCompareView, CompareListView

app_name = 'comparison'

urlpatterns = [
    path('add-to-compare/<int:product_id>/', AddToCompareView.as_view(), name='add_to_compare'),
    path('remove-from-compare/<int:product_id>/', RemoveFromCompareView.as_view(), name='remove_from_compare'),
    path('', CompareListView.as_view(), name='compared_products'),
]
