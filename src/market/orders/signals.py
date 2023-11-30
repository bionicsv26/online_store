from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from market.orders.models import Order


@receiver(m2m_changed, sender=Order.seller_products.through)
def count_order_cost(sender, instance, pk_set, action, **kwargs):
    """
    Сигнал, который высчитывает стоимость заказа, если заказ был создан или изменен.
    """
    if action != 'pre_add':
        instance.cost = sum(
            product.price
            for product in instance.seller_products.all()
        )
        instance.save()
