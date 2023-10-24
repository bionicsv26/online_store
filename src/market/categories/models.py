from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = 'name',

    name = models.CharField(max_length=20)
    parent = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE, related_name='categories')
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name
