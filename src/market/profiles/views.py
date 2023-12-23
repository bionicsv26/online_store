from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from market.banner_app.mixins import BannerSliderMixin
from market.categories.mixins import MenuMixin
from django.views.generic import (
    TemplateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)

class RegisterView(View):
    form_class = UserRegistrationForm
    initial = {'key': 'value'}
    template_name = 'profiles/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт для {username} создан.')

            return redirect(to='/')
        
        return render(request, self.template_name, {'form': form})

class AccountTemplateView(LoginRequiredMixin, TemplateView, BannerSliderMixin, MenuMixin):
    template_name = "profiles/account.html"


class ProfileTemplateView(LoginRequiredMixin, TemplateView, BannerSliderMixin, MenuMixin):
    template_name = "profiles/profile.html"
