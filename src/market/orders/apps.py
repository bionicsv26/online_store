from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market.orders'

    def ready(self):
        from .signals import count_order_cost_and_change_cart_discount
