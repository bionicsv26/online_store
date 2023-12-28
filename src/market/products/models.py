from django.db import models
from django.contrib.auth.models import User
from market.categories.models import Category
from django.urls import reverse


class ProductFeedback(models.Model):
    class Meta:
        ordering = [
            "user",
            "created_at",
        ]
        verbose_name = 'отзыв на продукт'
        verbose_name_plural = 'отзывы на продукт'
    user = models.ForeignKey(
        User,
        null=False,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    product = models.ForeignKey(
        'Product',
        null=False,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        )
    feedback_text = models.TextField()
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='отзыв создан',
    )

    def __str__(self):
        return f" Пользователь {self.user.username} оставил отзыв"



def image_directory_path(instance: 'Product', filename) -> str:
    return f'images/products/product_{instance.slug}/product_preview/{filename}'


class Product(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    name = models.CharField(max_length=20, verbose_name='название')
    preview = models.ImageField(null=True, unique=True, upload_to=image_directory_path, verbose_name='изображение')
    categories = models.ManyToManyField(Category, related_name='products', verbose_name='категории')
    description = models.TextField(verbose_name='описание')
    is_active = models.BooleanField(default=True, verbose_name='активирован')
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        preview_path = image_directory_path(self, self.preview)
        product = Product.objects.filter(preview=preview_path).first()
        if product is None:
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:product-details", kwargs={"product_slug": self.slug})
    

class ProductViewHistory(models.Model):
    class Meta:
        ordering = [
            "user",
            "product",
            "view_at",
        ]
        verbose_name = 'просмотр продукта'
        verbose_name_plural = 'просмотры продукта'
    user = models.ForeignKey(
        User,
        null=False,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    product = models.ForeignKey(
        Product, null=False,
        blank=True,
        on_delete=models.CASCADE,
        related_name='product_view_history',
        verbose_name='продукт'
    )
    view_at = models.DateField(
        auto_now_add=True,
        verbose_name='дата просмотра продукта',
    )

    def __str__(self):
        return f" Пользователь {self.name} просматривал продукт {self.product} {self.view_at}."