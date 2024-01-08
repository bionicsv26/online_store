from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save

from market.orders.models import Order, Cart


@receiver(m2m_changed, sender=Cart.seller_products.through)
def count_order_cost(sender, instance, action, **kwargs):
    """
    Сигнал, который высчитывает стоимость корзины, если заказ был создан или изменен.
    """
    if action != 'pre_add':
        instance.cost = sum(
            seller_product.get_discounted_price()
            for seller_product in instance.seller_products.all().select_related('discount')
        )
        instance.save()
