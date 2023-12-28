from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings

import requests

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def pay_handler_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        url = f"{settings.ORDERS_API_URL}{request.POST['pk']}/"
        r = requests.get(url)
        if r.status_code == 200:
            return JsonResponse({'paid': True})
        return JsonResponse({'paid': False})
