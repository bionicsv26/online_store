from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views, forms

app_name = 'market.profiles'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=forms.UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # password reset url-addresses
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=forms.UserSetPasswordForm), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('account/', views.AccountTemplateView.as_view(), name='account'),
    path('profile/', views.ProfileTemplateView.as_view(), name='profile'),
]
