# Generated by Django 5.1.5 on 2025-03-02 17:04

import core.product.utils
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0002_rename_name_category_category_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('product_name', models.CharField(max_length=100, unique=True)),
                ('product_description', models.CharField(max_length=500)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=10)),
                ('stock_quantity', models.PositiveIntegerField()),
                ('sku', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(upload_to=core.product.utils.get_product_photo_random_filename)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='category.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
