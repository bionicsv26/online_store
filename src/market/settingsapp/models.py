from django.db import models


class CacheTime(models.Model):
    categories_cache = models.IntegerField(default=86400)
    seller_data_cache = models.IntegerField(default=86400)
    banners_cache = models.IntegerField(default=600)
    products_cache = models.IntegerField(default=86400)
    top_products_cache = models.IntegerField(default=86400)
    product_data_cache = models.IntegerField(default=86400)

