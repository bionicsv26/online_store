from django.urls import path, include
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', )
]
