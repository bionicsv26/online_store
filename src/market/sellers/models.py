from django.db import models
from django.db.models import Q, Max

from market.categories.models import Category
from market.products.models import Product


def seller_logo_directory_path(instance: 'Seller', filename) -> str:
    return f'images/sellers/{instance.slug}/logo/{filename}'


class Seller(models.Model):
    class Meta:
        ordering = 'name',
        verbose_name = 'продавец'
        verbose_name_plural = 'продавцы'

    name = models.CharField(max_length=256, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    logo = models.ImageField(null=True, unique=True, upload_to=seller_logo_directory_path, verbose_name='лого')
    archived = models.BooleanField(default=False, verbose_name='архивация продавца')
    slug = models.SlugField(unique=True, verbose_name='slug')

    def __str__(self):
        return f'Продавец "{self.name}"'


class SellerProduct(models.Model):
    class Meta:
        verbose_name = 'продукт продавца'
        verbose_name_plural = 'продукты продавца'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='seller_products', verbose_name='продукт')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='seller_products', verbose_name='продавец')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    stock = models.IntegerField(default=0, verbose_name='сколько в наличии')
    discount = models.ForeignKey('Discount', on_delete=models.PROTECT, null=True, related_name='seller_products', verbose_name='скидка')
    created_at = models.DateField(auto_now_add=True, verbose_name='продукт продавца создан')

    def __str__(self):
        return f'Продукт продавца "{self.product.name}"'

    def get_discounted_price(self) -> float:
        return float(self.price) * (1 - self.discount.value / 100)

    def get_format_discounted_price(self) -> str:
        discounted_price = self.get_discounted_price()
        return '{:.2f}'.format(discounted_price)


class Discount(models.Model):
    class Meta:
        ordering = 'pk', 'value'
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'

    type = models.ForeignKey('DiscountType', null=True, on_delete=models.PROTECT, related_name='discounts', verbose_name='тип')
    value = models.IntegerField(default=0, verbose_name='скидка в %')
    amount_products = models.IntegerField(null=True, blank=True, verbose_name='количество товаров в корзине')
    categories = models.ManyToManyField(Category, blank=True, related_name='discounts', verbose_name='скидка на категории')
    expires = models.DateTimeField(null=True, blank=True, verbose_name='дата и время окончания скидки')

    def __str__(self):
        return f'Скидка с типом {self.type.name} на {self.value}%'


class DiscountType(models.Model):
    class Meta:
        verbose_name = 'тип скидки'
        verbose_name_plural = 'типы скидки'

    name = models.CharField(max_length=256, verbose_name='название')

    def __str__(self):
        return f'Тип скидки <{self.name}>'
