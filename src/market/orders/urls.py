from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import OrderDetailsView, OrderViewSet

app_name = 'orders'

router = DefaultRouter()
router.register('orders', OrderViewSet)

urlpatterns = [
    path('<int:pk>/', OrderDetailsView.as_view(), name='order_details'),
    path('api/', include(router.urls))
]
