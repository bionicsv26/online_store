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
from market.browsing_history_app.models import ProductBrowsingHistory
import logging

log = logging.getLogger(__name__)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['account_user_name'] = self.request.user

        browsing_history = (ProductBrowsingHistory.objects.
                                        prefetch_related('user', 'product').
                                        filter(user=self.request.user).
                                        order_by('-view_at')[:3]
                                        )
        context['brosing_history'] = browsing_history

        log.debug("Запуск рендеренга AccountTemplateView")
        log.debug("Контекст готов и передан на страницу account.html")
        return context

class ProfileTemplateView(LoginRequiredMixin, TemplateView, BannerSliderMixin, MenuMixin):
    template_name = "profiles/profile.html"
