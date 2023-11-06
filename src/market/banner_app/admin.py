from django.contrib import admin
from .models import BannerSlider


@admin.register(BannerSlider)
class BannerSliderAdmin(admin.ModelAdmin):
    list_display = ['product', 'title', 'text_short', 'created_at', 'is_active']

    list_display_links = 'product',
    search_fields = 'product', 'is_active'

    def text_short(self, obj: BannerSlider) -> str:
        if len(obj.text) < 48:
            return obj.text
        return obj.text[:48] + ' ...'

    text_short.short_description = "Краткий текст"  # Таким образом можно изменить имя поля
