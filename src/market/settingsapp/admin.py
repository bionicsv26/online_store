from django.contrib import admin
from .models import CacheTime


@admin.register(CacheTime)
class CacheTimeAdmin(admin.ModelAdmin):
    list_display = [
        'categories_cache', 'seller_data_cache', 'banners_cache',
        'products_cache', 'top_products_cache', 'product_data_cache'
    ]
