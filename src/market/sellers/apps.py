from django.apps import AppConfig


class SellersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market.sellers'

    def ready(self):
        from .signals import delete_cache, add_seller_product_discount
