from django.urls import path
from .views import (
    IndexTemplateView,
)

app_name = 'market.banner_app'

urlpatterns = [
    path('index/', IndexTemplateView.as_view(), name='index'),
]