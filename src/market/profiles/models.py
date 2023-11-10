from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    phone = models.CharField(max_length=10, blank=True)

    def __str__(self) -> str:
        return f'{self.user.username}'
