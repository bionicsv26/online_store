from django.contrib import admin

from .models import Order, OrderStatus


class OrderSellerProductInline(admin.StackedInline):
    model = Order.seller_products.through
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'pk', 'cost', 'delivery_address', 'status', 'created_at'
    list_display_links = 'pk',
    ordering = 'cost',
    inlines = [
        OrderSellerProductInline,
    ]
    fieldsets = (
        ('Required', {
            'fields': (
                'user',
                'full_name',
                'phone',
                'email',
                'seller_products',
                'cost',
                'status',
                'discount_type',
                'delivery_city',
                'delivery_address',
                'delivery_method',
                'payment_method',
            ),
        }),
    )


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'value'
    list_display_links = 'name',
