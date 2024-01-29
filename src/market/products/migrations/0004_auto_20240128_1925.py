# Generated by Django 3.2.22 on 2024-01-28 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20231221_2159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.SmallIntegerField(choices=[(1, 'Class'), (2, 'Model'), (3, 'Year release'), (4, 'Colour'), (5, 'Diagonal'), (6, 'Screen resolution'), (7, 'Matrix'), (8, 'Refresh rate'), (9, 'Pixel density'), (10, 'Ram'), (11, 'Internal memory')], default=7)),
                ('value', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='specification',
            field=models.ManyToManyField(related_name='specifications', to='products.Specification'),
        ),
    ]
