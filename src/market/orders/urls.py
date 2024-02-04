from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

app_name = 'orders'

router = DefaultRouter()
router.register('orders', views.OrderViewSet)

urlpatterns = [
    path('', views.OrdersHistoryView.as_view(), name='orders_history'),
    path('create/page_1/', views.MakingOrderPage1View.as_view(), name='making_an_order_page_1'),
    path('create/page_2/', views.MakingOrderPage2View.as_view(), name='making_an_order_page_2'),
    path('create/page_3/', views.MakingOrderPage3View.as_view(), name='making_an_order_page_3'),
    path('create/page_4/', views.MakingOrderPage4View.as_view(), name='making_an_order_page_4'),
    path('api/', include(router.urls)),
]
