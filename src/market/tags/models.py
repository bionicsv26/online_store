from django.db import models

from market.products.models import Product


class Tag(models.Model):
    class Meta:
        ordering = 'name',
        verbose_name = 'Тэг'
        verbose_name_plural = 'Теги'

    name = models.CharField(max_length=256, verbose_name='название')
    products = models.ManyToManyField(Product, related_name='tags', verbose_name='продукты')

    def __str__(self):
        return f'Тэг {self.name}'
