from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# TODO This part of code will be replaced by link to model in Category app due to MARKET-3 task
class Category(models.Model):
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = 'name',

    name = models.CharField(max_length=20)
    parent = models.ForeignKey('Category', null=True, blank=True, on_delete=models.PROTECT, related_name='categories')
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name


# TODO This part of code will be replaced by link to model in Product app due to MARKET-3 task
def image_directory_path(instance: models.Model, filename):
    return f'images/products/product_{instance.slug}/product_preview/{filename}'


class Product(models.Model):
    name = models.CharField(max_length=20)
    preview = models.ImageField(null=True, blank=True, upload_to=image_directory_path)
    category = models.ManyToManyField(Category, related_name='products')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name


# TODO This part of code will be replaced by link to model in Settings app due to MARKET-5 task
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
    # Banner name and banner image will be taken from Product
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
