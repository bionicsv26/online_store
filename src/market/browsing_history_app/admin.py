from django.contrib import admin
from .models import ProductBrowsingHistory


@admin.register(ProductBrowsingHistory)
class ProductBrowsingHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'view_at']

    list_display_links = 'user', 'product',
    search_fields = 'user', 'product',