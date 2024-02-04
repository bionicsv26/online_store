# Generated by Django 3.2.22 on 2024-02-04 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0009_auto_20240116_1549'),
        ('orders', '0005_auto_20240204_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='seller_products',
            field=models.ManyToManyField(related_name='orders', to='sellers.SellerProduct', verbose_name='продукты продавца'),
        ),
    ]
