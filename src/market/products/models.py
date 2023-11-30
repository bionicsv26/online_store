from django.db import models

from market.categories.models import Category


def image_directory_path(instance: 'Product', filename) -> str:
    return f'images/products/product_{instance.slug}/product_preview/{filename}'


class Product(models.Model):
    name = models.CharField(max_length=20)
    preview = models.ImageField(null=True, unique=True, upload_to=image_directory_path)
    categories = models.ManyToManyField(Category, related_name='products')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        preview_path = image_directory_path(self, self.preview)
        product = Product.objects.filter(preview=preview_path).first()
        if product is None:
            super().save(*args, **kwargs)
