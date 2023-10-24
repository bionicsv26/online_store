from django.apps import AppConfig
#from src.market.banner_app.signals import banner_slider_post_save_cash_reset, banner_slider_post_delete_cash_reset
from django.db.models.signals import post_save, post_delete

class BannerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market.banner_app'

    def ready(self):
        # importing model classes
        from .signals import banner_slider_post_save_cash_reset #, banner_slider_post_delete_cash_reset
        # Working when signals without decorator @reciver() - registering signals with the model's string label
        #post_save.connect(banner_slider_post_save_cash_reset, sender='banner_app.BannerSlider')
        #post_delete.connect(banner_slider_post_delete_cash_reset, sender='banner_app.BannerSlider')
