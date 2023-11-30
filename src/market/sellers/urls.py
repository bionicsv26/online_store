from django.urls import path

from market.sellers.views import SellerDetailsView, SellerListView

app_name = 'sellers'

urlpatterns = [
    path('', SellerListView.as_view(), name='sellers-list'),
    path('<slug:seller_slug>/', SellerDetailsView.as_view(), name='seller-details'),
]
