from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.core.cache import cache

from market.sellers.models import Seller, Discount, SellerProduct


@receiver(post_save, sender=Seller)
def delete_cache(sender, instance, **kwargs):
    """
    Сигнал, который удаляет кэш продавца, если продавец изменился.
    """
    seller_cache_name = f'seller_cache_{instance.slug}'
    seller_products_cache_name = f'seller_products_cache_{instance.slug}'

    seller_cache_data = cache.get(seller_cache_name)
    if seller_cache_data:
        cache.delete(seller_cache_name)

    seller_products_cache_data = cache.get(seller_products_cache_name)
    if seller_products_cache_data:
        cache.delete(seller_products_cache_name)


@receiver(m2m_changed, sender=Discount.categories.through)
def change_seller_product_discount(sender, instance, pk_set, action, **kwargs):
    """
    Сигнал, который изменяет тип скидки у SellerProduct в зависимости от того,
    добавляется ли категория товаров или удаляется из скидки с типом 3
    """
    discount_type_1 = Discount.objects.filter(type=1).first()
    if discount_type_1:
        seller_products = SellerProduct.objects.filter(
            Q(product__categories__id__in=pk_set) | Q(product__categories__parent__id__in=pk_set),
        )

        # добавление скидки с типом 1 к продуктам, категории которых удаляются из объекта скидки с типом 3
        if action == 'pre_remove':
            seller_products.update(discount=discount_type_1)

        # добавление скидки с типом 3 к продуктам, категории которых добавляются к объекту скидки с типом 3
        elif action == 'pre_add':
            seller_products.update(discount=instance)
