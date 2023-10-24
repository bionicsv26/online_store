from django.contrib import admin

from market.categories.models import Category
from market.products.models import Product


class ProductInline(admin.StackedInline):
    model = Product.category.through
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name'
    list_display_links = 'name',
    inlines = [
        ProductInline,
    ]
    prepopulated_fields = {'slug': ('name', )}
