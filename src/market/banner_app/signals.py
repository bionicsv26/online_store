from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache.utils import make_template_fragment_key
from .models import BannerSlider


@receiver(post_save, sender=BannerSlider)
def banner_slider_cash_reset(sender, instance, created, **kwargs) -> None:
    """
    This function clear the cache "slider_banners" from index.html page
    when model BannerSlider saved new information
    :param sender: model BannerSlider
    :param instance: model object
    :param created: boolean trigger of new model object creation
    :param kwargs: some additional information or parameters
    :return: None
    """
    key = make_template_fragment_key('slider_banners')
    cache.delete(key)


@receiver(post_delete, sender=BannerSlider)
def banner_slider_cash_reset(sender, instance, **kwargs) -> None:
    """
    This function clear the cache "slider_banners" from index.html page
    when some model BannerSlider objects were delisted
    :param sender: model BannerSlider
    :param instance: model object
    :param kwargs: some additional information or parameters
    :return: None
    """
    key = make_template_fragment_key('slider_banners')
    cache.delete(key)
