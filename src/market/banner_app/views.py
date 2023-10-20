from django.shortcuts import render
from django.http import (
    HttpRequest,
)
from django.views.generic import (
    TemplateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from .models import BannerSlider


def test_view_func(request: HttpRequest):
    return render(request, 'banner_app/test.html')

class IndexTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "banner_app/index.html"
    #context_object_name = 'purposes'




    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)

        context['banners_sliders'] = BannerSlider.objects.all()

        return context