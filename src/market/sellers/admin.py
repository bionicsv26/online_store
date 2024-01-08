from django.contrib import admin

from market.sellers.models import Seller, SellerProduct, Discount


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'description', 'archived'
    list_display_links = 'pk',
    ordering = 'pk', 'name', 'description'
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Обязательно', {
            'fields': ('name', 'description', 'logo'),
        }),
        ('Необязательно', {
            'fields': ('archived', 'slug'),
            'classes': {
                'collapse': True,
            }
        })
    )


@admin.register(SellerProduct)
class SellerProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'product', 'seller', 'price', 'stock', 'discount', 'created_at'
    list_display_links = 'pk',
    ordering = 'pk', 'price', 'stock', 'created_at'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'type', 'value'
    list_display_links = 'pk', 'name'
    ordering = 'pk', 'name'
    fieldsets = (
        ('Обязательные поля', {
            'fields': ('name', 'type', 'value'),
        }),
        ('Поля для скидки на количество товаров в корзине', {
            'fields': ('amount_products',),
            'classes': {
                'collapse': True,
            },
        }),
        ('Поля для скидки на категории товаров', {
            'fields': ('categories',),
            'classes': {
                'collapse': True,
            },
        }),
        ('Необязательные поля', {
            'fields': ('expires',),
            'classes': {
                'collapse': True,
            },
        }),
    )
