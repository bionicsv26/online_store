from django.urls import path

from market.sellers.views import SellerDetailsView

app_name = 'sellers'

urlpatterns = [
    path('<slug:seller_slug>/', SellerDetailsView.as_view(), name='seller-details'),
]
