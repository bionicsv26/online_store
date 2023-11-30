from django.db import models

from market.sellers.models import SellerProduct


class Order(models.Model):
    seller_products = models.ManyToManyField(SellerProduct, related_name='orders')
    cost = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True)
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey('OrderStatus', null=True, on_delete=models.PROTECT, related_name='orders')

    def __str__(self):
        return f'Заказ {self.pk}'


class OrderStatus(models.Model):
    class Meta:
        verbose_name = 'order status'
        verbose_name_plural = 'order statuses'

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
