from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import BannerSlider


@receiver(post_save, sender=BannerSlider)
def banner_slider_post_save_cash_reset(sender, instance, created, **kwargs) -> None:
    """
    This function clear the cache "slider_banners" from index.html page
    when model BannerSlider saved new information
    :param sender: model BannerSlider
    :param instance: model object
    :param created: boolean trigger of new model object creation
    :param kwargs: some additional information or parameters
    :return: None
    """
    print("DB BannerSlider was changed")
    some_cache = cache.get("banners_sliders_cache")
    if some_cache:
        cache.delete("banners_sliders_cache")



@receiver(post_delete, sender=BannerSlider)
def banner_slider_post_delete_cash_reset(sender, instance, **kwargs) -> None:
    """
    This function clear the cache "slider_banners" from index.html page
    when some model BannerSlider objects were delisted
    :param sender: model BannerSlider
    :param instance: model object
    :param kwargs: some additional information or parameters
    :return: None
    """
    print("One of the object was deleted from DB BannerSlider")
    if cache.get("banners_sliders_cache"):
        cache.delete("banners_sliders_cache")
