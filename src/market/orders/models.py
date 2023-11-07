from django.db import models

from market.products.models import Product


class Order(models.Model):
    products = models.ManyToManyField(Product, related_name='orders')
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True)
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey('OrderStatus', null=True, on_delete=models.PROTECT, related_name='orders')


class OrderStatus(models.Model):
    class Meta:
        verbose_name = 'order status'
        verbose_name_plural = 'order statuses'

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
