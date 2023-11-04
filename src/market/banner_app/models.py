from django.db import models
from django.contrib.auth.models import User
from market.products.models import Product


class BannerSlider(models.Model):
    class Meta:
        ordering = [
            "is_active",
            "created_at",
        ]
        verbose_name = 'банер слайдер'
        verbose_name_plural = 'банеры слайдеры'


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
