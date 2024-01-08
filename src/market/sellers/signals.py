from django.dispatch import receiver
from django.db.models.signals import post_save
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


@receiver(post_save, sender=Discount)
def add_seller_product_discount(sender, instance, **kwargs):
    if instance.type == 3:
        seller_products = SellerProduct.objects.filter(product__categories__discounts=instance)
        if not seller_products:
            seller_products = SellerProduct.objects.filter(product__categories__parent__discounts=instance)

        seller_products.update(discount=instance)
