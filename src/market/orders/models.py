from django.conf import settings
from django.db import models

from market.sellers.models import SellerProduct, DiscountType


class Order(models.Model):
    DELIVERY_METHOD_CHOICES = [
        ('ordinary', 'Обычная доставка'),
        ('express', 'Экспресс доставка')
    ]
    PAYMENT_METHOD_CHOICES = [
        ('online', 'Онлайн картой'),
        ('someone', 'Онлайн со случайного чужого счета')
    ]

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='orders', verbose_name='пользователь')
    cost = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='общая стоимость заказа')
    delivery_city = models.CharField(null=True, max_length=256, verbose_name='город заказчика')
    delivery_address = models.TextField(verbose_name='адрес заказчика')
    delivery_method = models.CharField(default=DELIVERY_METHOD_CHOICES[0], null=True, max_length=256, choices=DELIVERY_METHOD_CHOICES, verbose_name='способ доставки')
    payment_method = models.CharField(default=PAYMENT_METHOD_CHOICES[0], null=True, max_length=256, choices=PAYMENT_METHOD_CHOICES, verbose_name='способ оплаты')
    full_name = models.CharField(null=True, max_length=256, verbose_name='ФИО')
    phone = models.CharField(null=True, max_length=256, verbose_name='телефон')
    email = models.EmailField(null=True, verbose_name='почта')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время обновления заказа')
    status = models.ForeignKey('OrderStatus', null=True, on_delete=models.PROTECT, related_name='orders', verbose_name='статус заказа')
    order_products = models.ManyToManyField('OrderProduct', related_name='orders', verbose_name='продукт заказа')
    discount_type = models.ForeignKey(DiscountType, null=True, on_delete=models.PROTECT, related_name='order', verbose_name='тип скидки')

    def __str__(self):
        return f'Заказ {self.pk}'

    def check_paid(self):
        if self.status.value == 'paid':
            return True
        return False


class OrderProduct(models.Model):
    class Meta:
        verbose_name = 'продукт заказа'
        verbose_name_plural = 'продукты заказа'

    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE, related_name='order_products', verbose_name='продукт продавца')
    amount = models.PositiveIntegerField(verbose_name='количество')


class OrderStatus(models.Model):
    class Meta:
        verbose_name = 'статус заказа'
        verbose_name_plural = 'статусы заказа'

    value = models.CharField(null=True, max_length=256, verbose_name='значение')
    name = models.CharField(max_length=256, verbose_name='название')

    def __str__(self):
        return self.name
