from django.conf import settings
from django.db import models

from market.sellers.models import SellerProduct, Discount


class Order(models.Model):
    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='orders', verbose_name='пользователь')
    seller_products = models.ManyToManyField(SellerProduct, related_name='orders', verbose_name='продукты продавца')
    cost = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='общая стоимость заказа')
    delivery_city = models.CharField(null=True, max_length=256, verbose_name='город заказчика')
    delivery_address = models.TextField(verbose_name='адрес заказчика')
    delivery_method = models.CharField(null=True, max_length=256, verbose_name='способ доставки')
    payment_method = models.CharField(null=True, max_length=256, verbose_name='способ оплаты')
    full_name = models.CharField(null=True, max_length=256, verbose_name='ФИО')
    phone = models.CharField(null=True, max_length=256, verbose_name='телефон')
    email = models.EmailField(null=True, verbose_name='почта')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время обновления заказа')
    status = models.ForeignKey('OrderStatus', null=True, on_delete=models.PROTECT, related_name='orders', verbose_name='статус заказа')

    def __str__(self):
        return f'Заказ {self.pk}'


class OrderStatus(models.Model):
    class Meta:
        verbose_name = 'статус заказа'
        verbose_name_plural = 'статусы заказа'

    name = models.CharField(max_length=20, verbose_name='название')

    def __str__(self):
        return self.name


# временная сущность
class Cart(models.Model):
    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    seller_products = models.ManyToManyField(SellerProduct, related_name='carts', verbose_name='Продукт продавца')
    cost = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='Общая стоимость')
    discount = models.ForeignKey(Discount, null=True, on_delete=models.PROTECT, related_name='carts')

    def discounted_cart_cost(self) -> float:
        return float(self.cost) * (1 - self.discount.value / 100)

    def total_discounted_seller_products_price(self) -> float:
        return sum(
            seller_product.get_discounted_price()
            for seller_product in self.seller_products.all()
        )

    def priority_discounted_cost(self) -> str:
        cart_discount_cost = self.discounted_cart_cost()
        total_discounted_seller_products_price = self.total_discounted_seller_products_price()
        return '{:.2f}'.format(
            min((cart_discount_cost, total_discounted_seller_products_price)),
        )
