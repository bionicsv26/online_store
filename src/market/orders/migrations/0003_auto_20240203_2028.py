# Generated by Django 3.2.22 on 2024-02-03 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20240203_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstatus',
            name='value',
            field=models.CharField(max_length=256, null=True, verbose_name='значение'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_method',
            field=models.CharField(choices=[('ordinary', 'Обычная доставка'), ('express', 'Экспресс доставка')], default=('ordinary', 'Обычная доставка'), max_length=256, null=True, verbose_name='способ доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('online', 'Онлайн картой'), ('someone', 'Онлайн со случайного чужого счета')], default=('online', 'Онлайн картой'), max_length=256, null=True, verbose_name='способ оплаты'),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='name',
            field=models.CharField(max_length=256, verbose_name='название'),
        ),
    ]
