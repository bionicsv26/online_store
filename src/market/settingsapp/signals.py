from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver, Signal
from categories.models import Category


cache_clear = Signal()

@receiver(post_save, sender=Category)
def post_save_category(**kwargs):
    cache_clear.send_robust()
    print('Категория изменена, сброс кэша')

@receiver(post_delete, sender=Category)
def post_delete_category(**kwargs):
    cache_clear.send_robust()
    print('Категория удалена, сброс кэша')

@receiver(post_save, sender=Banner)
def post_save_banner(**kwargs):
    cache_clear.send_robust()
    print('Баннер изменен, сброс кэша')