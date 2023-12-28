from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = 'name',

    name = models.CharField(max_length=20, verbose_name='название')
    parent = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE, related_name='categories', verbose_name='категория')
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name
