from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d', help_text='Выбрать аватар профиля', verbose_name='Аватар профиля', null=True, blank=True, default='img/no_image.png')
    phone = models.CharField(max_length=256, help_text='Введите номер телефона', verbose_name='Номер телефона', null=True, blank=True)
    full_name = models.CharField(null=True, max_length=256, verbose_name='ФИО')

    def __str__(self) -> str:
        return f'{self.user.username}'
