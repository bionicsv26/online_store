from django.contrib import admin

from .models import (
    Product,
    ProductFeedback,
    ProductViewHistory,
)
from .models import Product, Specification, ProductImage


class ImagesInline(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'description',
    list_display_links = 'name',
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('specification', )
    inlines = [ImagesInline]


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'type', 'value'
    list_display_links = 'name',


@admin.register(ProductFeedback)
class ProductFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'short_feedback_text', 'created_at']

    list_display_links = 'user',
    search_fields = 'user',

    def short_feedback_text(self, obj: ProductFeedback) -> str:
        if len(obj.feedback_text) < 48:
            return obj.feedback_text
        return obj.feedback_text[:48] + ' ...'

    short_feedback_text.short_description = "Краткий текст отзыва"


@admin.register(ProductViewHistory)
class ProductViewHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'view_at']

    list_display_links = 'user', 'product',
    search_fields = 'user', 'product',
