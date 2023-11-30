from django.contrib import admin

from .models import Order, OrderStatus


class ProductInline(admin.StackedInline):
    model = Order.seller_products.through
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'pk', 'cost', 'delivery_address', 'status', 'comment', 'created_at'
    list_display_links = 'pk',
    ordering = 'cost', 'comment'
    inlines = [
        ProductInline,
    ]
    fieldsets = (
        ('Required', {
            'fields': ('seller_products', 'cost', 'status', 'delivery_address'),
        }),
        ('Extra', {
            'fields': ('comment',),
            'classes': {
                'collapse': True,
            },
        }),
    )


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name'
    list_display_links = 'name',
