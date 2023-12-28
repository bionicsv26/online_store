from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, MakingOrderPage1View, MakingOrderPage2View, MakingOrderPage3View, MakingOrderPage4View

app_name = 'orders'

router = DefaultRouter()
router.register('orders', OrderViewSet)

urlpatterns = [
    path('create/page_1/', MakingOrderPage1View.as_view(), name='making_an_order_page_1'),
    path('create/page_2/', MakingOrderPage2View.as_view(), name='making_an_order_page_2'),
    path('create/page_3/', MakingOrderPage3View.as_view(), name='making_an_order_page_3'),
    path('create/page_4/', MakingOrderPage4View.as_view(), name='making_an_order_page_4'),
    path('api/', include(router.urls)),
]
