from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market.profiles'

    # def ready(self):
    #     from .signals import count_cart_cost_and_change_cart_discount
