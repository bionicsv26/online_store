from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from market.settingsapp.signals import clear_cache
from django.dispatch import receiver
from .models import BannerSlider
import logging

log = logging.getLogger(__name__)

@receiver(post_save, sender=BannerSlider)
def banner_slider_post_save_cash_reset(sender, instance, created, **kwargs) -> None:
    """
    Эта функция receiver отчищает кэш" "banners_sliders_cache" для странице index.html
    когда в модели BannerSlider произошло сохранение
    :param sender: model BannerSlider
    :param instance: объект модели
    :param created: boolean тригер о создании нового объекта в модели
    :param kwargs: дополнительные параметры и переменные
    :return: None
    """
    log.debug("В БД BannerSlider произошло изменение. Вызван метод Save")
    some_cache = cache.get("banners_sliders_cache")
    if some_cache:
        cache.delete("banners_sliders_cache")
        log.debug("Кэш 'banners_sliders_cache' был удален")

@receiver(post_delete, sender=BannerSlider)
def banner_slider_post_delete_cash_reset(sender, instance, **kwargs) -> None:
    """
    Эта функция receiver отчищает кэш" "banners_sliders_cache" для странице index.html
    когда в модели BannerSlider был удален объект и об этом пришел сигнал
    :param sender: model BannerSlider
    :param instance: model object
    :param kwargs: дополнительные параметры и переменные
    :return: None
    """
    log.debug("В БД BannerSlider произошло изменение. Вызван метод Delete")
    if cache.get("banners_sliders_cache"):
        cache.delete("banners_sliders_cache")
        log.debug("Кэш 'banners_sliders_cache' был удален")

@receiver(clear_cache)
def banner_slider_admin_cash_reset(sender, **kwargs) -> None:
    """
    Эта функция receiver отчищает кэш" "banners_sliders_cache" для странице index.html
    когда в админ панели нажали кнопку "Clear cache"
    :param sender: signl clear_cache from settingsapp ?
    :param kwargs: дополнительные параметры и переменные
    :return: None
    """
    log.debug("В Админ панели была нажата кнопка Clean cache")
    some_cache = cache.get("banners_sliders_cache")
    if some_cache:
        cache.delete("banners_sliders_cache")
        log.debug("Кэш 'banners_sliders_cache' был удален")