from django.conf import settings
from django.db import models

# Create your models here.
class UserCart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_cart')
    items = models.JSONField()