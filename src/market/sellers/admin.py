from django.contrib import admin

from market.sellers.models import Seller, SellerProduct, Discount, DiscountType


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
    list_display = 'pk', 'type', 'value'
    list_display_links = 'pk',
    ordering = 'pk',
    fieldsets = (
        ('Обязательные поля', {
            'fields': ('type', 'value'),
        }),
        ('Поля для скидки на количество товаров в корзине', {
            'fields': ('amount_products',),
        }),
        ('Поля для скидки на категории товаров', {
            'fields': ('categories',),
        }),
        ('Необязательные поля', {
            'fields': ('expires',),
        }),
    )


@admin.register(DiscountType)
class DiscountTypeAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name'
    list_display_links = 'name',
    ordering = 'pk', 'name'
