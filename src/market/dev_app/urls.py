from django.urls import path
from .views import test_view_func

app_name = 'dev_app'

urlpatterns = [
    path('test/', test_view_func, name='test'),
]