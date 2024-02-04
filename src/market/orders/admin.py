from django.contrib import admin

from .models import Order, OrderStatus, OrderProduct


class OrderProductInline(admin.StackedInline):
    model = Order.order_products.through
    extra = 0


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
        OrderProductInline,
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


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'seller_product', 'amount'
    list_display_links = 'seller_product',
