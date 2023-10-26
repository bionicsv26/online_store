from django.apps import AppConfig

class BannerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market.banner_app'

    def ready(self):
        # importing model classes
        from .signals import (banner_slider_post_save_cash_reset,
                              banner_slider_post_delete_cash_reset,
                              )
