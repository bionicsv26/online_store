from django.db import models
from market.products.models import Product


def seller_logo_directory_path(instance: 'Seller', filename) -> str:
    return f'images/seller/seller_{instance.slug}/seller_logo/{filename}'


class Discount(models.Model):
    class Meta:
        ordering = [
            "type",
            "name",
            "value",
        ]
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'

    name = models.CharField(
        max_length=40,
        verbose_name='название скидки'
    )
    type = models.SmallIntegerField(
        default=0,
        verbose_name='тип скидки'
    )
    value = models.SmallIntegerField(
        default=0,
        verbose_name='сумма скидки'
    )

    def __str__(self):
        return self.name


class Seller(models.Model):
    class Meta:
        ordering = [
            "is_active",
            "name",
        ]
        verbose_name = 'продавец'
        verbose_name_plural = 'продавцы'

    name = models.CharField(
        max_length=40,
        verbose_name='продавец'
    )
    logo = models.ImageField(
        null=True,
        unique=True,
        upload_to=seller_logo_directory_path
    )
    description = models.TextField()
    is_active = models.BooleanField(
        default=True
    )
    slug = models.SlugField(
        max_length=40,
        unique=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        preview_path = seller_logo_directory_path(self, self.logo)
        seller = Seller.objects.filter(logo=preview_path).first()
        if seller is None:
            super().save(*args, **kwargs)


class SellerProduct(models.Model):
    class Meta:
        ordering = [
            "product",
            "price",
            "seller",
        ]
        verbose_name = 'продукт продавца'
        verbose_name_plural = 'продукты продавцов'

    product = models.ForeignKey(
        Product, null=False,
        blank=True,
        on_delete=models.CASCADE,
        related_name='seller_products',
        verbose_name='продукт'
    )
    seller = models.ForeignKey(
        Seller,
        null=False,
        blank=True,
        on_delete=models.CASCADE,
        related_name='sellers',
        verbose_name='продавец'
    )
    price = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        verbose_name='цена продукта'
    )
    discount = models.ForeignKey(
        Discount, null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='discounts',
        verbose_name='скидка'
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='продукт продавца создан',
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Продавец {self.seller} предлагает {self.product} по цене{self.price}."
