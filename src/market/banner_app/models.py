from django.db import models
from django.contrib.auth.models import User
from market.products.models import Product


# TODO Эта часть кода будет заменена на ссылку на модель из MARKET-5
class ProjectSettings(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name="Имя кэша",
    )
    banners_sliders_cache_timeout = models.SmallIntegerField(
        default=600,
        verbose_name="Время кэширования"
    )


class BannerSlider(models.Model):
    class Meta:
        ordering = [
            "user",
            "is_active",
            "created_at",
        ]
        verbose_name = 'банер слайдер'
        verbose_name_plural = 'банеры слайдеры'

    user = models.ForeignKey(
        User,
        null=False,
        on_delete=models.PROTECT,
        verbose_name='Создано пользователем',
    )
    # На банере имя продукта и его картинка буруться из модели Product
    product = models.OneToOneField(
        Product,
        on_delete=models.PROTECT
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный?'
    )

    title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Загаловок банера слайдера",
    )

    text = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Текст банера слайдера",
    )

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Создан'
    )

    def __str__(self):
        return self.product.name
