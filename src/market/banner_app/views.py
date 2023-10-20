from django.shortcuts import render
from django.http import (
    HttpRequest,
    HttpResponse,
)
# Create your views here.

def test_view_func(request: HttpRequest):
    return render(request, 'banner_app/test.html')