from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save

from market.orders.models import Order, Cart
from market.sellers.models import Discount


@receiver(m2m_changed, sender=Cart.seller_products.through)
def count_order_cost(sender, instance, action, **kwargs):
    """
    Сигнал, который считает стоимость корзины без скидки.
    """
    if action != 'pre_add':
        instance.cost = sum(
            seller_product.price
            for seller_product in instance.seller_products.all()
        )
        instance.save()


@receiver(m2m_changed, sender=Cart.seller_products.through)
def change_cart_discount(sender, instance, **kwargs):
    discount_type_1, discount_type_2 = Discount.objects.filter(Q(type=1) | Q(type=2))
    if discount_type_1 and discount_type_2:
        total_cart_seller_products = len(instance.seller_products.all())
        if total_cart_seller_products >= discount_type_2.amount_products:
            instance.discount = discount_type_2
        else:
            instance.discount = discount_type_1

        instance.save()
