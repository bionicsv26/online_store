from django.dispatch import receiver, Signal


clear_cache = Signal()

@receiver(clear_cache)
def my_callback(sender, **kwargs):
    print("Cache cleared!")

