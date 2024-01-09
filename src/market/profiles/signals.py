from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile
from ..orders.models import Cart
from ..sellers.models import Discount


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# временный сигнал создания корзины
@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        discount_type_2 = Discount.objects.filter(type=3).first()
        if discount_type_2:
            Cart.objects.create(user=instance, discount=discount_type_2)
