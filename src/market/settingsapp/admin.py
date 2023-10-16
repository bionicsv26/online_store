from django.contrib import admin
from .models import CacheTimes


@admin.register(CacheTimes)
class CacheTimesAdmin(admin.ModelAdmin):
    list_display = [
        'categories_cache', 'seller_data_cache', 'banners_cache',
        'products_cache', 'top_products_cache', 'product_data_cache'
    ]
