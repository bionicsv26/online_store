# Generated by Django 3.2.22 on 2023-12-02 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('banner_app', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannerslider',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='products.product'),
        ),
    ]
