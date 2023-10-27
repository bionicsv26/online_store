from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from .models import CacheTime
from .signals import clear_cache


@admin.register(CacheTime)
class CacheTimeAdmin(admin.ModelAdmin):
    list_display = [
        'categories_cache', 'seller_data_cache', 'banners_cache',
        'products_cache', 'top_products_cache', 'product_data_cache'
    ]
    change_list_template = "admin/cache_button_changelist.html"

    def get_urls(self):

        urls = super().get_urls()
        custom_urls = [
            path(
                'clear_cache/',
                 self.clear_cache,
                name='clear_cache'
            ),
        ]
        return custom_urls + urls

    def clear_cache(self, request):
        clear_cache.send_robust(sender=CacheTime)
        return HttpResponseRedirect("../")



