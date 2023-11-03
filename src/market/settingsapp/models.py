from django.db import models


class CacheTime(models.Model):
    categories_cache = models.IntegerField(default=86400, verbose_name="Время кэширования Категорий товаров")
    seller_data_cache = models.IntegerField(default=86400, verbose_name="Время кэширования данных о Продавце")
    banners_cache = models.IntegerField(default=600, verbose_name="Время кэширования Баннеров")
    products_cache = models.IntegerField(default=86400, verbose_name="Время кэширования списка Товаров из Каталога")
    top_products_cache = models.IntegerField(default=86400, verbose_name="Время кэширования списка Топ-Товаров")
    product_data_cache = models.IntegerField(default=86400, verbose_name="Время кэширования данных о Товаре")


