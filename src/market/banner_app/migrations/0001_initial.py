# Generated by Django 3.2.22 on 2023-11-18 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerSlider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный?')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='Загаловок банера слайдера')),
                ('text', models.CharField(blank=True, max_length=500, verbose_name='Текст банера слайдера')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Создан')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='products.product')),
            ],
            options={
                'verbose_name': 'банер слайдер',
                'verbose_name_plural': 'банеры слайдеры',
                'ordering': ['is_active', 'created_at'],
            },
        ),
    ]
