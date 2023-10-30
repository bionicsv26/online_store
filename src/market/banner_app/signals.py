from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import BannerSlider


@receiver(post_save, sender=BannerSlider)
def banner_slider_post_save_cash_reset(sender, instance, created, **kwargs) -> None:
    """
    Эта функция receiver отчищает кэш" "slider_banners" для странице index.html
    когда в модели BannerSlider произошло сохранение
    :param sender: model BannerSlider
    :param instance: объект модели
    :param created: boolean тригер о создании нового объекта в модели
    :param kwargs: дополнительные параметры и переменные
    :return: None
    """
    print("DB BannerSlider was changed")
    some_cache = cache.get("banners_sliders_cache")
    if some_cache:
        cache.delete("banners_sliders_cache")


@receiver(post_delete, sender=BannerSlider)
def banner_slider_post_delete_cash_reset(sender, instance, **kwargs) -> None:
    """
    Эта функция receiver отчищает кэш" "slider_banners" для странице index.html
    когда в модели BannerSlider был удален объект и об этом пришел сигнал
    :param sender: model BannerSlider
    :param instance: model object
    :param kwargs: дополнительные параметры и переменные
    :return: None
    """
    print("One of the object was deleted from DB BannerSlider")
    if cache.get("banners_sliders_cache"):
        cache.delete("banners_sliders_cache")
