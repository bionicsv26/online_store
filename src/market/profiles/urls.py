from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView
from . import views, forms


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=forms.UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # password changing url-addresses
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # password reset url-addresses
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('index/', TemplateView.as_view(template_name="profiles/index.html"), name='index'),
]
