from django.db import models
from django.contrib.auth.models import User

class ProductBrowsingHistory(models.Model):
    class Meta:
        ordering = [
            "user",
            "product",
            "view_at",
        ]
        verbose_name = 'история просмотра'
        verbose_name_plural = 'история просмотров'
    user = models.ForeignKey(
        User,
        null=False,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    product = models.ForeignKey(
        "products.Product",
        null=False,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        )
    view_at = models.DateField(
        auto_now_add=True,
        verbose_name='дата просмотра',
    )

    def __str__(self):
        return f" Пользователь {self.user.username} просмотрел товар {self.product.name}"

