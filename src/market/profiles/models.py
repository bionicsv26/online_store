from django.db import models
from django.conf import settings

from market.sellers.models import SellerProduct, Discount


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d', help_text='Выбрать аватар профиля', verbose_name='Аватар профиля', null=True, blank=True, default='img/no_image.png')
    phone = models.CharField(max_length=256, help_text='Введите номер телефона', verbose_name='Номер телефона', null=True, blank=True)
    full_name = models.CharField(null=True, max_length=256, verbose_name='ФИО')

    def __str__(self) -> str:
        return f'{self.user.username}'


# временная сущность
class Cart(models.Model):
    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    seller_products = models.ManyToManyField(SellerProduct, related_name='carts', verbose_name='Продукт продавца')
    cost = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='общая стоимость')
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.PROTECT, related_name='carts', verbose_name='скидка')

    def get_discounted_cost(self) -> float:
        return float(self.cost) * (1 - self.discount.value / 100)

    def get_total_discounted_seller_products_price(self) -> float:
        return sum(
            seller_product.get_discounted_price()
            for seller_product in self.seller_products.all().prefetch_related('discount')
        )

    def get_priority_discounted_cost(self) -> tuple[str, str]:
        cart_discount_cost = (self.get_discounted_cost(), 'cart_discount')
        total_discounted_seller_products_price = (self.get_total_discounted_seller_products_price(), 'category_discount')
        sorted_discounts = sorted((cart_discount_cost, total_discounted_seller_products_price))
        return '{:.2f}'.format(sorted_discounts[0][0]), sorted_discounts[0][1]
