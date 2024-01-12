from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from market.profiles.models import Cart
from market.sellers.models import Discount


@receiver(m2m_changed, sender=Cart.seller_products.through)
def count_order_cost_and_change_cart_discount(sender, instance, action, **kwargs):
    """
    Сигнал, который считает стоимость корзины без скидки и изменяет тип скидки корзины
    в зависимости от количества в ней продуктов.
    """
    if action in ('post_add', 'post_remove'):
        seller_products = instance.seller_products.all()

        # подсчет стоимости корзины без скидки
        instance.cost = sum(
            seller_product.price
            for seller_product in seller_products
        )
        instance.save()

        # изменение типа скидки корзины в зависимости от количества в ней продуктов
        discount_type_1, discount_type_2 = Discount.objects.filter(Q(type=1) | Q(type=2)).order_by('type')
        if discount_type_1 and discount_type_2:
            total_cart_seller_products = len(seller_products)
            if total_cart_seller_products >= discount_type_2.amount_products:
                instance.discount = discount_type_2
            else:
                instance.discount = discount_type_1

            instance.save()
